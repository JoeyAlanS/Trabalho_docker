#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
"""
API Link Extractor - Ruby com Cache Redis
Autor: Joey
"""

require 'sinatra'
require 'nokogiri'
require 'redis'
require 'json'

# Configurações
set :port, 4567
set :bind, '0.0.0.0'

# Conexão com Redis
redis = Redis.new(url: ENV['REDIS_URL'] || 'redis://localhost:6379')

# GET da raiz - instruções
get '/' do
  "Usage: http://<hostname>[:<port>]/api/<url>"
end

# GET para extrair links com cache
get '/api/*' do
  url = params['splat'][0]
  
  # Adicionar query string se existir
  query_string = request.query_string
  url += "?#{query_string}" if query_string != ""
  
  # Verificar cache
  cached = redis.get(url)
  
  if cached
    links = JSON.parse(cached)
  else
    # Extrair links
    begin
      response = HTTParty.get(url, timeout: 10)
      doc = Nokogiri::HTML(response.body)
      
      links = []
      doc.css('a').each do |link|
        href = link['href']
        # [FIX] Apenas adicionar se href existir (não nil/vazio)
        next unless href
        text = link.text.strip.split.join(' ')
        text = '[IMG]' if text.empty?
        
        links << {
          'text' => text,
          'href' => href
        }
      end
      
      # Armazenar em cache
      redis.set(url, JSON.generate(links))
    rescue => e
      puts "ERROR: #{e.class}: #{e.message}"
      links = []
    end
  end
  
  content_type :json
  JSON.pretty_generate(links)
end
