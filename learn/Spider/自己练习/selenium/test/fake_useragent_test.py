import fake_useragent


# def test_fake_useragent():
#     ua = fake_useragent.UserAgent().random
#     print(ua)
#     assert ua is not None

headers = {
    'User-Agent': fake_useragent.UserAgent().random
}


print(headers)