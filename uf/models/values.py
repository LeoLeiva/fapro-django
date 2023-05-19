from django.db import models

from uf.models import TimeStampedModel


class ValuesUF(TimeStampedModel):
    date = models.DateField(
        null=False,
        blank=False,
        db_index=True,
    )
    value = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        verbose_name="Precio de compra",
        default=0
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return '{} - {}'.format(self.date.strftime("%Y-%-m-%-d"), self.value)
