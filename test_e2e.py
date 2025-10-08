
import pytest
import subprocess
import time
from playwright.sync_api import Page, expect

# アプリケーションサーバーのベースURL
BASE_URL = "http://localhost:8000"

# テストセッション全体でFastAPIサーバーを起動・終了させるためのフィクスチャ
@pytest.fixture(scope="session", autouse=True)
def run_api_server():
    # uvicornサーバーをバックグラウンドプロセスとして起動
    server_process = subprocess.Popen(["venv/bin/uvicorn", "main:app"])
    
    # サーバーが起動するのを少し待つ
    time.sleep(2)
    
    # テスト実行
    yield
    
    # テスト終了後にサーバーを停止
    server_process.terminate()

def test_post_new_article_and_verify_in_list(page: Page):
    """
    ユーザーが新しい記事を投稿し、その記事が一覧に表示されることをテストする。
    """
    # 1. Webページにアクセス
    page.goto(BASE_URL)

    # ページタイトルが正しいことを確認
    expect(page).to_have_title("ブログ")

    # 2. フォームにテストデータを入力
    new_title = "Playwrightによるテスト投稿"
    new_content = "これはPlaywrightを使って自動的に投稿された記事です。"
    page.get_by_label("タイトル:").fill(new_title)
    page.get_by_label("本文:").fill(new_content)

    # 3. 「投稿する」ボタンをクリック
    page.get_by_role("button", name="投稿する").click()

    # 4. 記事一覧に、新しく投稿した記事のタイトルが表示されるのを待つ
    # locatorを使って、特定のテキストを持つli要素を取得
    new_post_in_list = page.locator(f"#post-list li:has-text('{new_title}')")

    # その要素が表示されることをアサート（待機も兼ねる）
    expect(new_post_in_list).to_be_visible(timeout=5000)

    # 念のため、最終的なテキスト内容も確認
    expect(new_post_in_list).to_contain_text(new_title)
