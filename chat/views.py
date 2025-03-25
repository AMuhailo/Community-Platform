from django.shortcuts import redirect, render, get_object_or_404
from chat.models import ChatGroup, GroupMessage
from chat.forms import MessageCreateForm
# Create your views here.


def index(request):
    chat_group = get_object_or_404(ChatGroup, name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]
    form = MessageCreateForm()
    if request.htmx:
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group
            message.author = request.user
            message.save()
            context = {
                'message':message,
                'user':request.user
            }
            return render(request,'page/chat/part/chat_message_p.html',context)
    context = {
        'group':chat_group,
        'messages':chat_messages,
        'form':form
    }
    return render(request,'page/chat/chat.html',context)

   