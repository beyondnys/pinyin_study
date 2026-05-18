-- TTS 语音资源表
USE pinyin_game;

CREATE TABLE IF NOT EXISTS `tts_audio_resource` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `biz_type` varchar(64) DEFAULT NULL COMMENT '业务类型',
  `biz_id` bigint DEFAULT NULL COMMENT '业务数据ID',
  `text_content` varchar(1000) NOT NULL COMMENT 'TTS 文本内容',
  `text_hash` varchar(64) NOT NULL COMMENT '文本hash，用于去重',
  `pinyin_text` varchar(1000) DEFAULT NULL COMMENT '关联拼音（展示用）',
  `voice_name` varchar(100) NOT NULL DEFAULT 'zh-CN-XiaoxiaoNeural' COMMENT 'TTS音色',
  `audio_bucket` varchar(100) NOT NULL COMMENT 'MinIO bucket',
  `audio_object_name` varchar(500) NOT NULL COMMENT 'MinIO object name',
  `audio_url` varchar(1000) DEFAULT NULL COMMENT '最近一次预签名访问地址',
  `audio_format` varchar(20) NOT NULL DEFAULT 'mp3' COMMENT '音频格式',
  `generate_status` tinyint NOT NULL DEFAULT 0 COMMENT '0待生成 1生成中 2成功 3失败',
  `fail_reason` varchar(1000) DEFAULT NULL COMMENT '失败原因',
  `retry_count` int NOT NULL DEFAULT 0 COMMENT '重试次数',
  `enabled_flag` tinyint NOT NULL DEFAULT 1 COMMENT '1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_by` bigint DEFAULT NULL COMMENT '创建人',
  `updated_by` bigint DEFAULT NULL COMMENT '更新人',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '软删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_text_hash_voice` (`text_hash`, `voice_name`),
  KEY `idx_biz` (`biz_type`, `biz_id`),
  KEY `idx_generate_status` (`generate_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='TTS语音资源表';
