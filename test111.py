async def Msg_Text(self, Event:events) -> dict:
    # 其他现有代码保持不变...
    msg_id = Event.message.id
    
    # 确定group_id
    if isinstance(Event.message.to_id, PeerChannel):
        group_id = int(Event.message.to_id.channel_id)
    elif isinstance(Event.message.to_id, PeerChat):
        group_id = int(Event.message.to_id.chat_id)
    else:
        group_id = ""
        
    if group_id != "":
        group_id_str = self.Channel_id_fix(group_id)
        # 提取纯数字部分并取绝对值
        if isinstance(group_id_str, str) and group_id_str.startswith("-100"):
            clean_group_id = abs(int(group_id_str[4:]))
        else:
            clean_group_id = abs(int(group_id_str) if isinstance(group_id_str, str) else group_id)
        

    
    # 将更新后的msg_id应用到text_info字典中
    text_info = {
        "msg_text": msg_text,
        "sender_id": sender_id,
        "group_id": group_id_str if group_id != "" else "",
        "msg_id": msg_id,
        "grouped_id": grouped_id,
        # 其他字段...
    }
    
    return text_info