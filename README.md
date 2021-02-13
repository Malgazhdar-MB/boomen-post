# boomen-post
* Для правильной работы рекомендуется python 3.6
* Используем редактор PyCharm
* Для исправной работы обратной связи:
  1. В файле settings.py в параметр EMAIL_HOST_USER напишите свой email, и в EMAIL_HOST_PASSWORD его пароль
  2. В файле views.py в процедуре contactMail измените эл. почты под шаблон
     def contactMail(request):
        if request.method == 'POST':
          form = ContactForm(data=request.POST)
          if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'ваш мэйл',
                ['мэйл на которого хотите отправить обратную связь'],
                fail_silently=True
            )
