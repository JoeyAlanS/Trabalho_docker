#!/usr/bin/env ruby
# encoding: utf-8

require "sinatra"
require "open-uri"
require "uri"
require "nokogiri"
require "json"
require "timeout"

set :protection, :except => :path_traversal

Dir.mkdir("logs") unless Dir.exist?("logs")
cache_log = File.new("logs/extraction.log", "a")

get "/" do
  "Usage: http://<hostname>[:<prt>]/api/<url>"
end

get "/api/*" do
  url = [params["splat"].first, request.query_string].reject(&:empty?).join("?")
  jsonlinks = JSON.pretty_generate(extract_links(url))
  cache_log.puts "#{Time.now.to_i}\tNOCACHE\t#{url}"

  status 200
  headers "content-type" => "application/json"
  body jsonlinks
end

def extract_links(url)
  links = []
  options = {
    "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }
  timeout(10) do
    doc = Nokogiri::HTML(open(url, options))
    doc.css("a").each do |link|
      text = link.text.strip.split.join(" ")
      begin
        links.push({
          text: text.empty? ? "[IMG]" : text,
          href: URI.join(url, link["href"]),
        })
      rescue StandardError
        # skip malformed href
      end
    end
  end
  links
end
