FROM openjdk:8-jre-slim

# Install JMeter
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz && \
    tar -xzf apache-jmeter-5.5.tgz && \
    mv apache-jmeter-5.5 /opt/jmeter && \
    rm apache-jmeter-5.5.tgz && \
    apt-get remove -y wget && \
    apt-get autoremove -y && \
    apt-get clean

# Set JMeter home
ENV JMETER_HOME /opt/jmeter
ENV PATH $JMETER_HOME/bin:$PATH

# Create directories
RUN mkdir -p /tests /results

# Copy test files
COPY jmeter-performance-test/jmeter/*.jmx /tests/

# Set working directory
WORKDIR /tests

# Entry point
ENTRYPOINT ["jmeter"]
CMD ["-n", "-t", "/tests/login_lead_assignm.jmx", "-l", "/results/results.jtl", "-e", "-o", "/results/html-report"]