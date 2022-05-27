from glom import glom

# Contact manager examples

from glom.tutorial import *

contact = Contact("Julian", emails=[Email(email="jlahey@svtp.info")], location="Canada")
contact.save()

target = Contact.objects.all()
print(len(target), "contacts")

spec = {
    "results": [
        {
            "id": "id",
            "name": "name",
            "add_date": ("add_date", str),
            "emails": (
                "emails",
                [{"id": "id", "email": "email", "type": "email_type"}],
            ),
            "primary_email": Coalesce("primary_email.email", default=None),
            "pref_name": Coalesce("pref_name", "name", skip="", default=""),
            "detail": Coalesce(
                "company", "location", ("add_date.year", str), skip="", default=""
            ),
        }
    ]
}

resp = glom(target, spec)
# uncomment to see the result of the full spec above
print(json.dumps(resp, indent=2, sort_keys=True))
