# Фикс битого slug: "Автоюрист в Севастополе" имел slug "yurist-v-sevastopole",
# дублирующий slug города -> кривой URL. Переименовываем в "avtoyurist-v-sevastopole"
# и ставим 301-редирект со старого адреса. Идемпотентно и безопасно на любой БД.

from django.db import migrations

OLD_SLUG = "yurist-v-sevastopole"
NEW_SLUG = "avtoyurist-v-sevastopole"


def fix_slug(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")

    # Только страница-услуга (depth=4) со старым slug; сам город (depth=3) не трогаем.
    page = Page.objects.filter(slug=OLD_SLUG, depth=4).first()
    if page is None:
        return  # уже переименовано или такой страницы нет — выходим

    old_url_path = page.url_path  # напр. /home/yurist-v-sevastopole/yurist-v-sevastopole/
    page.slug = NEW_SLUG
    if old_url_path and old_url_path.rstrip("/").endswith(OLD_SLUG):
        parent_path = old_url_path.rstrip("/").rsplit("/", 1)[0]
        page.url_path = parent_path + "/" + NEW_SLUG + "/"
    page.save(update_fields=["slug", "url_path"])

    # 301-редирект со старого публичного URL на новый, чтобы не терять вес/индекс.
    try:
        Redirect = apps.get_model("wagtailredirects", "Redirect")
        old_public = old_url_path.replace("/home", "", 1).rstrip("/")  # /yurist-v-sevastopole/yurist-v-sevastopole
        if old_public and not Redirect.objects.filter(old_path=old_public).exists():
            Redirect.objects.create(
                old_path=old_public,
                redirect_page_id=page.id,
                is_permanent=True,
            )
    except Exception:
        # Если приложение редиректов недоступно — переименование уже сделано, это не критично.
        pass


def reverse_slug(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    page = Page.objects.filter(slug=NEW_SLUG, depth=4).first()
    if page is None:
        return
    page.slug = OLD_SLUG
    if page.url_path and page.url_path.rstrip("/").endswith(NEW_SLUG):
        parent_path = page.url_path.rstrip("/").rsplit("/", 1)[0]
        page.url_path = parent_path + "/" + OLD_SLUG + "/"
    page.save(update_fields=["slug", "url_path"])


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_contactspage_policypage_pricepage_uslugipage"),
        ("wagtailcore", "0001_initial"),
        ("wagtailredirects", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(fix_slug, reverse_slug),
    ]
