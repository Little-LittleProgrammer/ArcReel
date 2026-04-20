# 万相-参考生视频2.7

模型:  wan2.7-r2v

## 步骤1：创建任务获取任务ID

### 请求参数

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-r2v",
    "input": {
        "prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ",
        "media": [
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
            },
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "duration": 10,
        "prompt_extend": false,
        "watermark": true
    }
}'
```

### 响应参数

```json
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

## 步骤 2 根据任务ID查询结果

### 请求

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应

```json
{
    "request_id": "52cade0d-905e-9b7d-a01e-xxxxxx",
    "output": {
        "task_id": "18814247-f944-4102-aa4a-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-04-02 22:53:19.537",
        "scheduled_time": "2026-04-02 22:53:30.427",
        "end_time": "2026-04-02 23:00:39.287",
        "orig_prompt": "视频2抱着图片3在咖啡厅里弹奏一支舒缓的美式乡村民谣，视频1笑着看着视频2，并缓缓向他走去",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?xxxx"
    },
    "usage": {
        "duration": 15,
        "input_video_duration": 5,
        "output_video_duration": 10,
        "video_count": 1,
        "SR": 720,
        "ratio": "16:9"
    }
}
```