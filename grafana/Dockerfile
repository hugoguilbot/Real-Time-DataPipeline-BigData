FROM grafana/grafana:latest

# Installe un plugin pour Cassandra
# Remplacez `nom-du-plugin-cassandra` par le nom correct du plugin
RUN grafana-cli plugins install hadesarchitect-cassandra-datasource

# Copie les configurations de provisioning dans le conteneur
COPY ./provisioning /etc/grafana/provisioning

# Copie les dashboards dans le conteneur
COPY ./dashboards /var/lib/grafana/dashboards