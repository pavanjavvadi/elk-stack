FROM docker.elastic.co/logstash/logstash:7.14.0

# copy the jdbc jar file
COPY ./compose/logstash/postgresql-42.2.23.jar /usr/share/logstash/logstash-core/lib/jars/postgresql.jar


# # copy lib database jdbc jars
# COPY ./compose/logstash/postgresql-42.2.23.jar /usr/share/logstash/logstash-core/lib/jars/postgresql.jar

# # remove default pipeline.yml file
# RUN rm -rf /config/pipelines.yml

# COPY . .


