from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Summary(models.Model):
    PROTOCOL = "Протокол встречи"
    SUMMARY = "Саммари записи"
    RESUME = "Резюме консультации"
    CONTENT = "Содержание лекции"
    SCRIPT_CHOICES = (
        (PROTOCOL, "Протокол встречи"),
        (SUMMARY, "Саммари записи"),
        (RESUME, "Резюме консультации"),
        (CONTENT, "Содержание лекции"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    link = models.CharField(max_length=100, verbose_name='ссылка')
    transcription = models.TextField(verbose_name='транскрипция', **NULLABLE)
    summary = models.TextField(verbose_name='саммари', **NULLABLE)
    is_ready = models.BooleanField(default=False, verbose_name="результат готов")
    worker_db_id = models.IntegerField(verbose_name='ИД результата в БД воркера', **NULLABLE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время запроса')
    script = models.CharField(max_length=40, choices=SCRIPT_CHOICES, default=SUMMARY, verbose_name='сценарий обработки')
    prompt = models.TextField(verbose_name='Промпт пользователя', **NULLABLE)

    def __str__(self):
        return f'{self.user}, {self.link}'

    class Meta:
        verbose_name = 'запрос к воркеру'
        verbose_name_plural = 'запросы к воркеру'
