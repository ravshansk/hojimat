FROM ruby:2.4.1
RUN mkdir /code
WORKDIR /code
ADD Gemfile /code/Gemfile
ADD Gemfile.lock /code/Gemfile.lock
RUN bundle
ADD . /code 
