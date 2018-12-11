---
layout: default
title: Articles on Management 
permalink: /management
---

# Articles on Management

<div class="posts">
{% for post in site.tags["management"] %}
<div class="listpost">
<h3 class="post-title"><a href="{{ site.baseurl }}{{ post.url }}">{{post.title}}</a></h3>
<span class="post-date">{{ post.date | date_to_string }}</span>
{{ post.excerpt }}
{% if post.excerpt != post.content %}
<a href="{{ site.baseurl }}{{ post.url }}">Read more...</a>
{% endif %}
</div>
{% endfor %}
</div>
