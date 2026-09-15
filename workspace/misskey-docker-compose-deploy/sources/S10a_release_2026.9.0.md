# Release 2026.9.0 2026-09-06T11:19:39Z

> [!IMPORTANT]
> 今回のアップデートでは重大な脆弱性を修正しています。可及的速やかにアップデートしてください。
>
> This update contains serious vulnerability fixes. Please update to this or the latest version of Misskey as soon as possible.

### Note
- カスタム絵文字の一括インポートは、必要なロールポリシーを所持しているかどうかにかかわらず、管理者権限を持つユーザーのみが実行できるようになりました。
- `notes/reactions` を GET で取得することができなくなりました。

### General
- Enhance: ノート翻訳時、CWも翻訳対象に含めるように
- Enhance: 依存関係の更新
- Enhance: 翻訳の更新

### Client
- Enhance: 画像ビューワーで、ピクセルアートの拡大表示に適したモードを追加（画像ビューワー起動時に画面上の詳細メニューから有効化できます）
- Enhance: メディアリスト上でぼかしを解除したメディアを画像ビューワーで表示した際にぼかしを解除した状態で表示するように
- Enhance: 音声プレイヤーを画像・動画ビューワーに統合
- Enhance: パフォーマンスの向上
- Fix: 画像の表示時にBlurhashが描画されない場合があるのを修正
- Fix: モバイルでの利用時に一部のテキストが選択できない問題を修正
- Fix: 「利用できるリアクションを先頭に表示」が機能しない問題を修正
- Fix: コントロールパネルでユーザーをメール検索し見つからなかった場合、エラーダイアログが2重に表示される問題を修正
- Fix: リストにユーザーを追加/削除した際、メンバー数の表示が更新されない問題を修正
- Fix: 通知トーストの位置を左側にした場合でも右から通知が入ってくる問題を修正
- Fix: 通知トーストのアニメーションの挙動が不安定になる問題を修正

### Server
- Feat: `.well-known/change-password`に対応（`/settings/security`にリダイレクトします）
- Enhance: アクセストークンでAPIを使用している際に、自身のアクセストークンを失効させることができるように
  - `i/revoke-token` エンドポイントにリクエストすることで、現在使用しているアクセストークンを失効させることができます
- Fix: 既にミュートしているスレッドに対して再度スレッドミュートを作成しようとするとサーバーエラーになる問題を修正
- Fix: 古いバージョンのMisskeyで作成されたアカウントでノートの連合が行えない場合があるのを修正
- Fix: 一部のWebSocketチャンネルのクリーンアップ処理が正しく行われない問題を修正
- Fix: セキュリティに関する修正
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-rrm8-pwmf-gxm3
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-5c3q-jmv3-r6fx
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-vwfw-pgg7-5hg6
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-xc6c-m4f7-jcc9
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-jx9q-24fh-4fxw
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-h3mq-w9gq-6mwm
  - https://github.com/misskey-dev/misskey/security/advisories/GHSA-g3ph-65m3-x625
