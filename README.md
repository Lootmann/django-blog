# django-blog

HTML,CSS はガン無視 よくわからん<br>
機能だけを実装<br>

## Model

```python
from django.db import models


class CustomUser:
    pass


class BlogTag(models.Model):
    name = models.CharField(max_length=100)


class Blog:
    title = models.CharField(max_length=150)
    content = models.TextField()
    is_public = models.BooleanField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    clicked_counter = models.PositiveIntegerField()
    likes = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # features
    tags = models.ManyToManyField(BlogTag)
```

## TODO List

### app:blogs

- [x] PageIndex
  - [x] 他人が `is_public` にしている blog だけを表示する
  - [x] `blog.content` の表示は文字数制限をつける
- [x] BlogIndex
  - [x] いい感じに見やすく表示する
  - [x] `content` をクリックしたらDetailに飛ぶ
  - [x] 自分が author であるブログだけを表示する
- [x] BlogDetail
  - [x] 権限を持つAuthorにだけ Edit, Delete に遷移できるように許可する
- [x] BlogCreate
  - [x] Authentication + Permission (LoginRequiredMixinを利用すればOK)
- [x] BlogUpdate
- [x] BlogDelete
- [ ] BlogSearch
  - `content` で文字列検索
  - `BlogTag` で検索
- [x] Form
  - [x] CreateForm
  - [x] UpdateForm
  - [x] DeleteForm
- [ ] tests

### Features

- [ ] サイドバーなど
  - 多分これをタグと連携して このタグはいくつのブログがありますよ -><br>
    `Django(21)`など そんな感じで使うと良い<br>
    templatetags で表示する感じ?


### now implementing

:^)

### Done

- [x] 公開・非公開機能
  - [x] いわゆる下書き機能と同等? `is_public` でそれを行う

- [x] BlogModel自体に `CustomUserModel` をつける
  - ログインしないと見るだけしか無理など 他人のブログは編集できないなど超基本的なシステム
  - Permission をつけて 公開非公開、編集作成などをログインしないとできないようにする

- [x] 閲覧回数の表示
  - Blogs.Model 自体に `counter` みたいなやつを設定してクリックされるたびに<br>
    カウントする感じで これは簡単にできる(た)

- [x] 何分くらいで読めます表示
  - 文字数でカウントすればよいか blog を表示するたびに文字数を計算すると負担が大きいので<br>
    （とはいえ `len(blog.content)` とするだけ）`Create`, `Update` する時に<br>
    Model 自体に文字数を `PositiveIntegerField` で入れるとパフォーマンスいい感じかも<br>
    そもそもこれ必要かなという話 文字数だけ表示? そうするともっと分かりづらいか
  - やっぱり `len(blog.content)` だけにする そんなに重い関数でもなさそうだろう

- [x] いいね！みたいなやつ
  - `Like`は `LikeModel` にデータ入れておくと良い?
    - [x] `LikeModel` が必要と思いきや `likes = models.ManyToManyField(CustomUser, ...)`で<br>
      だけで行けることが判明 とてもきれいに実装が可能な予感
    - [x] `click` したら APIを飛ばして `like` の部分だけを更新する JavaScript を使ってみる<br>
      いわゆる `Ajax` と呼ばれる技術
    - [x] JavaScript `fetch` を利用する<br>
      使い方間違ってるのは分かるが一応動いているので終了 そのうち別ファイルにJs分割する

- [x] ブログを `Markdown` で表示 and かけるようにする
  - third party を利用するのが吉 text -> html に変換するプラグインは大量にあることが判明
  - `programming language highlighting` も同時に行う

- [x] blogs/update.html css<br>
  - Content記載する枠が狭すぎるので限界まで広くする
  - ようやくCSSを理解し始めた が、最初から全部作り直したい さっさとcss framework 使えるようになりましょう

## Never Impl Lists D:

- お気に入り Favorites機能 -> やることLikesと大して変わらんので実装せずに終了
- ログインしてないやつは全文読ませない機能 -> content short で表示して文章の最後にLoginのリンク見せるだけなので終了
- タグ機能 -> 実装に時間かかる感じがするので次のアプリ作る時に ManyToManyField の検索機能を追加する
  - がそんなに難しくないっていうか `MtM.filter(...)` で出力されたやつをTemplate に渡すだけなので簡単にできる
  - Templates で タグをいい感じに表示するのが面倒なだけ JavaScript の機能を利用することになる
- 各Authorが書いたBlogだけを表示する機能: 基本的にな search の機能なので実装せず終了

## Bug Fix

- [x] Updated, Deleted Permission をちゃんとする
  別のユーザーが作ったBlogのEditやDeleteができてしまっている！<br>
  Update, Delete は get, post 時に `logged in user` と<br>
  blog.author.id と比較する必要があり<br>
  - [x] Blog.UpdateView
  - [x] Blog.DeleteView

- [ ] ReadCount 更新時に `updated_at` が変化する
  - updated_at は 当然 `blog.content` の更新時のみに更新される `DateTimeField`なので<br>
    こいつはまずい どうにかする 更新の意味を深く考えてなかった
