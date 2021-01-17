---
layout: archive
classes: wide

title: About
permalink: /about/
---

# About Me

***Author*** :  {{ site.author.name }}  
***Mail*** :  [{{ site.email }}](mailto:{{ site.email }})  

{{ site.author.bio }}

# Social Links
{% for link in site.author.links %}<i class="fas {{ link.icon }} fa-fw" >[{{ link.label }}]({{ link.url }}){: target="_blank"}</i>  
{% endfor %}