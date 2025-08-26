# Sift Home Assistant Custom Component

This is a prototype custom component to ingest Home Assistant data into Sift's Hardware Observability Platform (https://siftstack.com/)

## Installation

Copy `custom_components/sift/` in this repo to `<config_dir>/custom_components/sift/` where `<config_dir>` is where your Home Assistant unique configurations are stored (for example where configuration.yaml is stored)

Once the custom component is installed in the correct directory, add the following to your `configuration.yaml` file in your `<config_dir>`. Also, ensure you are using the correct API URI, API KEY and ASSET for your specific Sift deployment.

```yaml
sift:
  api_uri: https://<uri>/api/v2/ingest
  api_key: <token>
  asset: my_hass_asset_name
```

Users can also filter what data is ingested into Sift. For example:

```yaml
sift:
  api_uri: https://<uri>/api/v2/ingest
  api_key: <token>
  asset: my_hass_asset_name
  filter:
    include_domains:
      - sensor
    exclude_domains:
      - number
      - media_player
      - weather
      - todo
      - switch
```

## Technical Notes

* This is a prototype and must be manually installed into Home Assistant. Future iterations can formalize this as an offiical [Home Assistant Integration](https://www.home-assistant.io/integrations/?brands=featured) or [HACS](https://www.hacs.xyz).
* This component uses Sift's [Schemaless Ingestion](https://docs.siftstack.com/docs/ingestion/schemaless-ingestion) API. Enumerated data types will show up as log data in Sift.
