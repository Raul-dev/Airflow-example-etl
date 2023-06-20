https://www.mariotalavera.com/nifi/2019/09/08/nifi-01-copying-records-between-tables


  # version control for nifi flows
  registry:
      hostname: myregistry
      container_name: registry_container
      image: 'apache/nifi-registry:1.15.0'  # latest image as of 2021-11-09.
      restart: on-failure
      ports:
          - 18080:18080
      environment:
          - LOG_LEVEL=INFO
          - NIFI_REGISTRY_DB_DIR=/opt/nifi-registry/nifi-registry-current/database
          - NIFI_REGISTRY_FLOW_PROVIDER=file
          - NIFI_REGISTRY_FLOW_STORAGE_DIR=/opt/nifi-registry/nifi-registry-current/flow_storage
      volumes:
          - ./images/nifi/nifi_registry/database:/opt/nifi-registry/nifi-registry-current/database
          - ./images/nifi/nifi_registry/flow_storage:/opt/nifi-registry/nifi-registry-current/flow_storage
      healthcheck:
          test: ["CMD", "curl", "-f", "http://myregistry:18080/nifi-registry/"]
          interval: 30s
          timeout: 20s
          retries: 3          

volumes:
    nifi-database_repository:
    nifi-flowfile_repository:
    nifi-content_repository:
    nifi-provenance_repository:
    nifi-state:
    nifi-conf: