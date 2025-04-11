import os
import time
import json
import random
import datetime
import pandas as pd
import requests
current_path = os.path.dirname(os.path.abspath(__file__))

params = {
'device_platform': 'webapp',
'aid': '6383',
'channel': 'channel_pc_web',
'aweme_id': '7001739262597106978',
'cursor': '0',
'count': '10',
'item_type': '0',
'insert_ids': '',
'whale_cut_token': '',
'cut_version': '1',
'rcFT': '',
'update_version_code': '170400',
'pc_client_type': '1',
'pc_libra_divert': 'Windows',
'support_h265': '1',
'support_dash': '1',
'version_code': '170400',
'version_name': '17.4.0',
'cookie_enabled': 'true',
'screen_width': '1707',
'screen_height': '1068',
'browser_language': 'zh-CN',
'browser_platform': 'Win32',
'browser_name': 'Chrome',
'browser_version': '127.0.0.0',
'browser_online': 'true',
'engine_name': 'Blink',
'engine_version': '127.0.0.0',
'os_name': 'Windows',
'os_version': '10',
'cpu_core_num': '32',
'device_memory': '8',
'platform': 'PC',
'downlink': '10',
'effective_type': '4g',
'round_trip_time': '50',
'webid': '7477561235329926667',
'uifid': '973a3fd64dcc46a3490fd9b60d4a8e663b34df4ccc4bbcf97643172fb712d8b09bc364c606eecceaf76cba933f5ee58db827bf36665104d0291c829e054010c690655172224895f56e281b32da6425cd3794d0604a188e7d0060d08cb4055b2551f9d195a3197d3f271c7afb8f5fa58b2987c44ce5c64768b82b3927dbc15abb23e3656f07c4c1535999c042ffcac2c2254292b17eeec52adb9721100b383e9f',
'msToken': '-B27503cU96_HVgWxnyy8t60RulO9F85yWz7Cnt8uAkQOy_EwBQx7dSTg1GewTruV6mYeu65zfmec4OFj_nnwodYbAxi6205T7jJQs7Hfyj2MRKEa17uxrfC5iuKyVAVQcPWVYryJbMZRkBv3MKqFdcaZcUPh-B_-s_zrKXwsV3elT99Ep5-rjs=',
'a_bogus': 'D6sVgFWixdAnFdKtYKEOyXpUkqj/rTSy3PTKR7cUtPxTGhFc4RNAqre9JoqsdPJOS8B0wq/73xUlGnVbQt7zZH9pLmkkus4jc4/cIS8oMqhvY4iZJH8pebtxwk-PUuTT8QICEZURAsMEIx25IrCiApptw/lNB5mDKZ-UVAuCO92RUAujwx/9a5jsiw7q8D=='
}

headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      'cookie':'SEARCH_RESULT_LIST_TYPE=%22single%22; ttwid=1%7CbFA4nWq26APCaw-t5_cZFYpcEyMvwfI1QNTm31qPVeU%7C1741005414%7Cfe3b0d11d8906416b42c8a5ee3e6de026380770e6a62f63e71fe37825626817f; hevc_supported=true; fpk1=U2FsdGVkX19a+fVauhJl1ewNtTA+j1VDvnX2MG2fxN+y3cH/3gnAzuWlQuamvtIv1Z2zSqapJKIQ6w40SgwZKA==; fpk2=362d7fe3d8b2581bffa359f0eeda7106; passport_csrf_token=f1d66b8ceb180efaf5a2ba4eb2a40cca; passport_csrf_token_default=f1d66b8ceb180efaf5a2ba4eb2a40cca; __security_mc_1_s_sdk_crypt_sdk=4827a5fc-4c76-a762; bd_ticket_guard_client_web_domain=2; UIFID=973a3fd64dcc46a3490fd9b60d4a8e663b34df4ccc4bbcf97643172fb712d8b09bc364c606eecceaf76cba933f5ee58db827bf36665104d0291c829e054010c690655172224895f56e281b32da6425cd3794d0604a188e7d0060d08cb4055b2551f9d195a3197d3f271c7afb8f5fa58b2987c44ce5c64768b82b3927dbc15abb23e3656f07c4c1535999c042ffcac2c2254292b17eeec52adb9721100b383e9f; s_v_web_id=verify_m8e5uskh_DQv13ICY_c63x_45IU_8Ehm_ZVCX3cY65gwP; is_dash_user=1; xgplayer_user_id=326352087704; xgplayer_device_id=52312106849; d_ticket=9083c79ecc91224fddaa144e175b4a395789e; n_mh=3W_NX18PdB34B0eM91Z1hl9eKaDM9cdYtV8wZk4nvxU; __security_mc_1_s_sdk_sign_data_key_sso=342c5ef0-475f-b8a4; __security_mc_1_s_sdk_cert_key=b8ed75c5-40d3-98b4; passport_auth_status=8c893a58cfcdaf6fca3ee255a5ab356c%2C; passport_auth_status_ss=8c893a58cfcdaf6fca3ee255a5ab356c%2C; SelfTabRedDotControl=%5B%5D; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region=cn-js; store-region-src=uid; passport_mfa_token=CjcKbXqFlIXxJY%2BNeETVWQcs3yBxJ3IdznWu7Req0%2Bs830zofaIsHUWop4tLKTAPnekzzyBAL6GpGkoKPAAAAAAAAAAAAABOyC7hifdyqow1bveMPdIuP0oiuEkAIrpuhPxiNr0h5HfacQyM0PKacMJYDU2zm5mskhCnzewNGPax0WwgAiIBA7MSsbQ%3D; passport_assist_user=CkFz679QjDM0PdNt4AgcUlw3_48K87QnOJiLX6X2q4smfnLhXF5oQ-j7il1uwR-UQmVbMjsJnKy5v0p2qjRY4Ng3xRpKCjwAAAAAAAAAAAAATshvTH1VfBJGmID3YcBvCYmgLNcvglR2JXW3wsfolqRAwDc82rgFEjPYQ3aPaAI2TCUQ_MvsDRiJr9ZUIAEiAQMK0nam; sid_guard=6228e4111d0e59ed5d8c0b6db2b8fe87%7C1742550156%7C5184000%7CTue%2C+20-May-2025+09%3A42%3A36+GMT; uid_tt=d4df5e115ea438d02c00ab1aa1930e78; uid_tt_ss=d4df5e115ea438d02c00ab1aa1930e78; sid_tt=6228e4111d0e59ed5d8c0b6db2b8fe87; sessionid=6228e4111d0e59ed5d8c0b6db2b8fe87; sessionid_ss=6228e4111d0e59ed5d8c0b6db2b8fe87; is_staff_user=false; sid_ucp_v1=1.0.0-KDAzMzJhYzc5NDNkNGRjOTQxYzExYjNjZjNmNTg3ZDZhMDEyM2IxNzkKIQiOqqCZo4y-BxCM6fS-BhjvMSAMMJnojIkGOAVA-wdIBBoCbGYiIDYyMjhlNDExMWQwZTU5ZWQ1ZDhjMGI2ZGIyYjhmZTg3; ssid_ucp_v1=1.0.0-KDAzMzJhYzc5NDNkNGRjOTQxYzExYjNjZjNmNTg3ZDZhMDEyM2IxNzkKIQiOqqCZo4y-BxCM6fS-BhjvMSAMMJnojIkGOAVA-wdIBBoCbGYiIDYyMjhlNDExMWQwZTU5ZWQ1ZDhjMGI2ZGIyYjhmZTg3; login_time=1742550149636; __security_mc_1_s_sdk_sign_data_key_web_protect=5f54ad55-48a3-aff1; _bd_ticket_crypt_cookie=624e2907ebfb7bc4f380a2e994ef66a6; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.313%7D; publish_badge_show_info=%220%2C0%2C0%2C1743570126592%22; dy_swidth=1707; dy_sheight=1068; strategyABtestKey=%221743910086.17%22; douyin.com; device_web_cpu_core=32; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1068%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A32%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A3.55%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; xg_device_score=7.6544903604636865; download_guide=%223%2F20250406%2F0%22; WallpaperGuide=%7B%22showTime%22%3A1743947888314%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAK0DbY6_-TaCr91JErhyDehnO7iiFzSmsLir9t2PE4pySfEN-5WzkAwPjGFsohzcK%2F1743955200000%2F0%2F0%2F1743949092545%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_signature=_02B4Z6wo00f01Q0BUxgAAIDA0XjMrsdDM-UNIVeAACS1f3; csrf_session_id=6baf36cd5949e7109a315f01ab415d14; home_can_add_dy_2_desktop=%221%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAK0DbY6_-TaCr91JErhyDehnO7iiFzSmsLir9t2PE4pySfEN-5WzkAwPjGFsohzcK%2F1743955200000%2F0%2F1743949222428%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSWRqR09UYVNZWk8xaFdsa3Vlb0RkYlFaTzdmZlNWbDB1aEx0N3VqY1hiU2ZvL1F3dTduR2Y0RVJ5ZWtKWmhZRHM1cVdUekRYdm1wRmplUlhHcnJVcUk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; odin_tt=f7cb0e249478cf83d7e986d5ff2f5cf41d95eb7fdb0fca11f47eca741f50db2b7a2bbcb132bfb01919da671129f3c98dc220bcab2295169fdb0d6bc9f07d7022; passport_fe_beating_status=true; IsDouyinActive=true',
      'referer':'https://www.douyin.com/'}

def get_comments(video_id, cursor=0, count=50):
  url = f"https://www.douyin.com/aweme/v1/web/comment/list?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={video_id}&cursor={cursor}&count={count}"
  response = requests.get(url, headers=headers, params=params)
  if response.status_code == 200:
      return response.json()
  else:
      print("Failed to get comments")
      return None

comments_id_json_path = os.path.join(current_path,'comments_id.json')
with open (comments_id_json_path,'r',encoding='utf-8') as f:
    videos_data = json.load(f)

comments_integration = []
for video in videos_data:
    print(f"当前采集的视频url为：{video['video_url']}")
    comments_data = []
    video_id = video['comment_id']
    for i in range(1000):
        time.sleep(random.randint(10, 20))
        comments_json = get_comments(video_id,cursor=i*50, count=50)
        if comments_json:
            print(f'正在采集第{i+1}')
        else:
            print(f'{comments_json}为空，结束获取评论，开始存储')
            break
        try:
            for comment in comments_json['comments']:
                timestamp = comment['create_time']
                dt = datetime.datetime.fromtimestamp(timestamp)
                single_comment = {
                    'user': comment['user']['nickname'],
                    'text': comment['text'],
                    'create_time': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'digg_count': comment['digg_count'],
                    'region': comment['user']['region'],
                }
                comments_data.append(single_comment)
                comments_integration.append(single_comment)
        except Exception as e:
            print(f"comments_json['comments']为：{comments_json['comments']}:")
            break

    # 写入csv文件
    dir_path = os.path.join(current_path,'data')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_name = os.path.join(dir_path,video['video_name']+'.csv')
    df = pd.DataFrame(comments_data)
    df.to_csv(file_name, index=False, encoding='utf-8-sig')

integration_name = os.path.join(current_path,'data','AI_输10亿合集.csv')
df = pd.DataFrame(comments_integration)
df.to_csv(integration_name, index=False, encoding='utf-8-sig')
