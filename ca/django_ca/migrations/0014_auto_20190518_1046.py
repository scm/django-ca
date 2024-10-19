# Generated by Django 2.2.1 on 2019-05-18 10:46

from django.db import migrations


def remove_empty(apps, schema_editor):
    Certificate = apps.get_model("django_ca", "Certificate")
    Certificate.objects.filter(revoked_reason="").update(revoked_reason="unspecified")
    CertificateAuthority = apps.get_model("django_ca", "CertificateAuthority")
    CertificateAuthority.objects.filter(revoked_reason="").update(revoked_reason="unspecified")


class Migration(migrations.Migration):
    dependencies = [
        ("django_ca", "0013_certificateauthority_crl_number"),
    ]

    operations = [
        migrations.RunPython(remove_empty, migrations.RunPython.noop),
    ]
