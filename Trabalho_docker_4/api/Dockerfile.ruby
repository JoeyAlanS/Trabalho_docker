FROM ruby:2.6
LABEL maintainer="Joey"

ENV REDIS_URL="redis://localhost:6379"

WORKDIR /app
COPY Gemfile /app/
RUN bundle install

COPY linkextractor.rb /app/main.rb
RUN chmod a+x /app/main.rb

CMD ["ruby", "./main.rb"]
