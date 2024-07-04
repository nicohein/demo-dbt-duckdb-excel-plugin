with source as (

    select * from {{ source('excel_source_via_plugin', 'raw_customers') }}

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select * from renamed
