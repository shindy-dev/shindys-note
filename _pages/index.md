---
layout: single
classes: wide
author_profile: true
toc: true
toc_label: "Table of Contents"
share: true

title: Home
permalink: /
---
<!-- 更新履歴ボックス -->
<style type="text/css">
    .kousin {
        overflow:auto;
        height:256px;
        margin-top: 32px;
        margin-bottom: 32px;
        font-size: 16px;
    }
</style>


# はじめに

{% highlight cmd %}
> Hello World!
{% endhighlight %}
当サイトではプログラミングをしていて「ふ～ん」と思ったことから普段使いそうなツールの紹介まで、自由に投稿していきます！  
※メモ代わりでもあるため、記事によって質にムラがあります。ご了承ください。  
[記事一覧]({{ site.baseurl }}/articles/)へ

# 更新履歴
<div class="kousin">
    {% for post in site.posts limit:10 %}
        {% assign update_date = post.date | date: "%B %-d %Y" %}
        {% assign upload_date = post.upload_date | date: "%B %-d %Y" %}
        {% if update_date != upload_date %}
<font color="#00C000">[UPDATE]</font>  {{ update_date }} :
        {% else %}
<font color="#ff4500">[UPLOAD]</font> {{ upload_date }} :
        {% endif %}
<a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a> <br>
    {% endfor %}
</div>

# 今まで勉強してきた言語
- **Programing**
    - **C言語**  
        最初に勉強した言語。正直もう覚えてない。

    - **C++**  
        ゼミ配属されてから使い始めた言語。この言語でオブジェクト指向を勉強。  
        ImGuiというGUIライブラリで色々作ってた。

    - **Java**  
        android使いとしてある程度コードは読めた方がいいだろうと勉強してる。

    - **Python**  
        ゼミでメインに使ってた言語。機械学習で使うと思いきやGUIを作ってた。  
        簡単（楽）にかけるし大好きな言語の一つ。

    - **Kotlin**  
        Javaと同じ理由だけど、新しい言語！って感じで面白そうだったから勉強した。結構好き。

    - **VB.Net**  
        最近勉強中の言語。今までGUI開発向けでない言語で作ってたからかなり開発が捗りそう。

    - **C#**  
        Unity使ったことないのに質問されたから勉強してみた。VB.Netとほとんど変わらない。  
        Unityに関してはモデル作るのが面倒で2Dしか触れてない。
    
    - **JavaScript**  
        ElectronでGUI作ったときにさらっと勉強

    - **Swift**  
        さらっと基本文法を勉強
    
    - **Flutter**  
        Dart言語を使ってクロスプラットフォーム開発が可能なプラットフォーム。楽にアプリ作りたいならこれ。

- **Markup**
    - **HTML**, **CSS**  
        高校の情報の授業で触ったことがあるくらい。Web系は詳しくない。

    - **kv言語**  
        PythonのGUIライブラリ「Kivy」でGUIを作成するときにレイアウトや基本動作を楽に設定できるマークアップ言語。CSSに近いのかな。