from .models import Menu, Post


# def menu_urls(request):
#     print('...menu_urls context_processors works...')
#     menu_urls = Menu.objects.all()
#     print('urls in database:', len(menu_urls))
#     # print(menu_urls)
#     menu_dict = {}
#     for url in menu_urls:
#         menu_dict[url.url_code] = {'url': url.url, 'title': url.title}
#     print(menu_dict)
#     return {'page_urls': menu_dict,}

def footer_news(request):
    print('...footer_news...working')
    posts = Post.objects.filter(publish_in_basement=True).order_by('-published_date')[:3]
    return {'basement_news': posts }
