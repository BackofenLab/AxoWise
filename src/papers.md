---
title: Papers
layout: page
permalink: /papers
---

<ul>
{% for post in site.categories["papers"] %}
<li>
    <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
</li>
{% endfor %}
</ul>