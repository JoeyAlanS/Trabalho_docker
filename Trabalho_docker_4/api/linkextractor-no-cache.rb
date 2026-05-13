#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
"""
API Link Extractor - Ruby SEM Cache Redis
Autor: Joey
"""

require 'sinatra'
require 'nokogiri'
require 'json'

# Configurações
set :port, 4567
set :bind, '0.0.0.0'

# GET da raiz - instruções
get '/' do
  "Usage: http://<hostname>[:<port>]/api/<url>"
end

# GET para extrair links (SEM cache)
get '/api/*' do
  url = params['splat'][0]
  
  # Adicionar query string se existir
  query_string = request.query_string
  url += "?#{query_string}" if query_string != ""
  
  # Extrair links direto (sem cache)
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
  rescue => e
    puts "ERROR: #{e.class}: #{e.message}"
    links = []
  end
  
  content_type :json
  JSON.pretty_generate(links)
end
