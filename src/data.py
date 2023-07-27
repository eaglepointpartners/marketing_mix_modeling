import duckdb as db
import pandas as pd

BENCHMARK_DATA_PATH = '/root/data/daily_benchmark_metrics.parquet'

def build_regression_data_from_benchmark_org(org_id: str, grain: str = 'daily') -> pd.DataFrame:

    # base table
    benchmark_metrics = db.sql(
        f"""
        select
            benchmark_organisation_id,
            organisation_gmv_bucket,
            vertical_name,
            vertical_category_name,
            territory,
            sub_territory,
            channel_grouping,
            channel_platform,
            day_date,
            date_trunc('week', day_date) as week_date,
            sessions,
            new_users,
            orders,
            new_orders,
            orders_units,
            new_orders_units,
            orders_product_net_revenue as net_revenue,
            new_orders_product_net_revenue as new_net_revenue,
            orders_product_original_price as original_price,
            new_orders_product_original_price as new_original_price,
            orders_product_gross_discount as orders_discount,
            new_orders_product_gross_discount as new_orders_discount,
            marketing_spend,
            marketing_impressions
        from '{BENCHMARK_DATA_PATH}'
        where benchmark_organisation_id = '{org_id}'
        """
    )

    group_by_date = 'week_date' if grain == 'weekly' else 'day_date'
 
    # assemble organisation attributes
    attributes = db.sql(
        """
        with org_territories as (
            select
                benchmark_organisation_id,
                sub_territory,
                sum(orders) as orders,
                sum(net_revenue) as revenue
            from benchmark_metrics
            group by benchmark_organisation_id, sub_territory
        ),
        org_top_territories as (
            select
                benchmark_organisation_id,
                sub_territory as top_territory,
                revenue / orders as aov
            from org_territories
            qualify row_number() over (
                    partition by benchmark_organisation_id
                    order by revenue desc
                ) = 1
        ),
        other_attributes as (
            select distinct
                benchmark_organisation_id,
                organisation_gmv_bucket,
                vertical_name,
                vertical_category_name
            from benchmark_metrics
        )
        select
            a.benchmark_organisation_id,
            a.top_territory,
            a.aov,
            b.organisation_gmv_bucket as gmv_bucket,
            b.vertical_name as vertical,
            b.vertical_category_name as sub_vertical
        from org_top_territories a
        join other_attributes b
            on a.benchmark_organisation_id = b.benchmark_organisation_id
        """
    )

    # demand variables
    demand = db.sql(
        f"""
        select
            benchmark_organisation_id,
            {group_by_date},
            sum(sessions) as sessions,
            sum(new_users) as new_sessions,
            sum(new_orders) as acquisitions,
            sum(new_orders_units) as acquisition_orders_units,
            sum(new_net_revenue) as acquisition_net_revenue,
            sum(new_original_price) as acquisition_original_price,
            sum(new_orders_discount) as acquisition_orders_discount
        from benchmark_metrics
        group by
            benchmark_organisation_id,
            {group_by_date}
        """
    )

    # marketing variables
    marketing = db.sql(
        f"""
        with assign_channel as (
            select
                benchmark_organisation_id,
                {group_by_date},
                case
                    when channel_platform ilike 'google' then
                        case
                            when channel_grouping ilike '%shopping%' then 'google_shopping'
                            when channel_grouping ilike '%paid search%' then 'google_search'
                            when channel_grouping ilike '%display%' then 'google_display'
                            when channel_grouping ilike '%performance max%' then 'google_pmax'
                            when channel_grouping ilike '%video%' then 'google_video'
                            else 'other'
                        end
                    when channel_platform ilike 'facebook' then 'meta'
                    when channel_platform ilike 'audience network' then 'meta'
                    when channel_platform ilike 'instagram' then 'meta'
                    when channel_platform ilike 'messenger' then 'meta'
                    else 'other'
                end as marketing_channel,
                sessions,
                new_users,
                marketing_spend,
                marketing_impressions
            from benchmark_metrics
        )
        pivot assign_channel
        on marketing_channel in (
                'meta',
                'google_search',
                'google_shopping',
                'google_display',
                'google_pmax',
                'google_video'
            )
        using
            sum(marketing_spend) as spend,
            sum(marketing_impressions) as imps,
            sum(sessions) as clicks,
            sum(new_users) as new_clicks
        """
    )

    # put it all together
    regression_data = db.sql(
        f"""
        select
            attributes.*,
            {', '.join([
                    'demand.' + c for c in demand.columns
                    if c.lower() != 'benchmark_organisation_id'
                ])
            },
            {', '.join([
                    'marketing.' + c for c in marketing.columns
                    if c.lower() not in ('benchmark_organisation_id', group_by_date)
                ])
            }
        from attributes
        join demand
            on attributes.benchmark_organisation_id = demand.benchmark_organisation_id
        left join marketing
            on attributes.benchmark_organisation_id = marketing.benchmark_organisation_id
            and demand.{group_by_date} = marketing.{group_by_date}
        order by attributes.benchmark_organisation_id, demand.{group_by_date}
        """
    )
    regression_data = regression_data.df()
    regression_data.columns = regression_data.columns.str.lower()

    # remove historical data until there is non-zero cummulative spend
    regression_data = regression_data.set_index(['benchmark_organisation_id',group_by_date]).sort_index()
    regression_data['cumm_spend'] = regression_data.filter(like='_spend').sum(axis=1).groupby(level=0).cumsum()
    regression_data = regression_data[regression_data.cumm_spend > 0].reset_index()

    return regression_data.fillna(0.0)
