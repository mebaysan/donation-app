from django.http import HttpResponse
import csv


def get_csv_response_of_queryset(queryset, filename):
    """Returns a CSV response with the given queryset and filename.

     Args:
            queryset (Queryset) : a Django queryset
            filename (str): filename of the CSV file
    Returns:
            HttpResponse
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}.csv"
    writer = csv.writer(response)

    # automatically generate header row by using queryset.model
    writer.writerow([field.verbose_name for field in queryset.model._meta.fields])

    # write data row by row. If the field is related, it will write its related models' __str__ method
    for row in queryset:
        writer.writerow(
            [
                getattr(row, field.name)
                if not field.related_model
                else "{} - {}".format(
                    getattr(row, field.name).__str__(), getattr(row, field.name).id
                )
                for field in queryset.model._meta.fields
            ]
        )

    return response
