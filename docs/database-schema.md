# 当前 Supabase 数据库结构存档

本文件由当前 Supabase PostgreSQL 元数据导出整理而成，用于 PersonaWeaver 复赛仓库迁移和数据库结构核对。真实数据库密码、API Key、连接串不会写入本文档。

## 数据库概况

- PostgreSQL：`PostgreSQL 17.6 on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 15.2.0, 64-bit`
- 导出 schema：`public`
- public 表数量：`9`
- public 函数数量：`116`

## 已启用扩展

- `hypopg`：`1.4.1`
- `index_advisor`：`0.2.0`
- `pg_stat_statements`：`1.11`
- `pgcrypto`：`1.3`
- `plpgsql`：`1.0`
- `supabase_vault`：`0.3.1`
- `uuid-ossp`：`1.1`
- `vector`：`0.8.0`

## 表结构

### `public.auth_sessions`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `auth_id` | `text` | `NO` | `gen_prefixed_id('s'::text)` |  |
| `user_id` | `text` | `NO` | `` |  |
| `access_token_jti` | `text` | `NO` | `` |  |
| `refresh_token_hash` | `text` | `NO` | `` |  |
| `expires_at` | `timestamp with time zone` | `NO` | `` |  |
| `revoked_at` | `timestamp with time zone` | `YES` | `` |  |
| `created_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `updated_at` | `timestamp with time zone` | `NO` | `now()` |  |

约束：
- `CHECK` `2200_17892_1_not_null`：``
- `CHECK` `2200_17892_2_not_null`：``
- `CHECK` `2200_17892_3_not_null`：``
- `CHECK` `2200_17892_4_not_null`：``
- `CHECK` `2200_17892_5_not_null`：``
- `CHECK` `2200_17892_7_not_null`：``
- `CHECK` `2200_17892_8_not_null`：``
- `FOREIGN KEY` `auth_sessions_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `auth_sessions_pkey`：`auth_id`
- `UNIQUE` `auth_sessions_access_token_jti_key`：`access_token_jti`

索引：
- `auth_sessions_access_token_jti_key`：`CREATE UNIQUE INDEX auth_sessions_access_token_jti_key ON public.auth_sessions USING btree (access_token_jti)`
- `auth_sessions_pkey`：`CREATE UNIQUE INDEX auth_sessions_pkey ON public.auth_sessions USING btree (auth_id)`
- `idx_auth_sessions_expires_at`：`CREATE INDEX idx_auth_sessions_expires_at ON public.auth_sessions USING btree (expires_at)`
- `idx_auth_sessions_user_id`：`CREATE INDEX idx_auth_sessions_user_id ON public.auth_sessions USING btree (user_id)`

触发器：
- `trg_auth_sessions_updated_at`：`BEFORE UPDATE`

### `public.books`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `book_id` | `text` | `NO` | `gen_prefixed_id('b'::text)` |  |
| `user_id` | `text` | `NO` | `` |  |
| `title` | `text` | `NO` | `` |  |
| `author` | `text` | `YES` | `` |  |
| `source_type` | `text` | `NO` | `` |  |
| `language` | `text` | `YES` | `'zh-CN'::text` |  |
| `status` | `text` | `NO` | `'pending'::text` |  |
| `book_file_url` | `text` | `NO` | `` |  |
| `created_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `updated_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `progress` | `numeric` | `YES` | `` | 人物提取进度条 |
| `err_message` | `text` | `YES` | `` |  |

约束：
- `CHECK` `2200_17912_10_not_null`：``
- `CHECK` `2200_17912_1_not_null`：``
- `CHECK` `2200_17912_2_not_null`：``
- `CHECK` `2200_17912_3_not_null`：``
- `CHECK` `2200_17912_5_not_null`：``
- `CHECK` `2200_17912_7_not_null`：``
- `CHECK` `2200_17912_8_not_null`：``
- `CHECK` `2200_17912_9_not_null`：``
- `CHECK` `books_status_check`：``
- `FOREIGN KEY` `books_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `books_pkey`：`book_id`

索引：
- `books_pkey`：`CREATE UNIQUE INDEX books_pkey ON public.books USING btree (book_id)`
- `idx_books_status`：`CREATE INDEX idx_books_status ON public.books USING btree (status)`
- `idx_books_user_id`：`CREATE INDEX idx_books_user_id ON public.books USING btree (user_id)`

触发器：
- `trg_books_updated_at`：`BEFORE UPDATE`

### `public.card`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `card_id` | `text` | `NO` | `` |  |
| `book_id` | `text` | `NO` | `` |  |
| `type` | `text` | `NO` | `` |  |
| `name` | `text` | `NO` | `` |  |
| `intro` | `text` | `YES` | `` |  |
| `created_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |
| `updated_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |
| `prompt_id` | `text` | `YES` | `` |  |
| `content_local_url` | `text` | `YES` | `` |  |
| `content_oss_url` | `text` | `YES` | `` |  |

约束：
- `CHECK` `2200_20610_10_not_null`：``
- `CHECK` `2200_20610_1_not_null`：``
- `CHECK` `2200_20610_3_not_null`：``
- `CHECK` `2200_20610_4_not_null`：``
- `CHECK` `2200_20610_5_not_null`：``
- `CHECK` `2200_20610_9_not_null`：``
- `FOREIGN KEY` `card_book_id_fkey`：`book_id` → `public.books(book_id)`
- `FOREIGN KEY` `card_prompt_id_fkey`：`prompt_id` → `public.prompt_config(prompt_id)`
- `PRIMARY KEY` `card_pkey`：`card_id`

索引：
- `card_pkey`：`CREATE UNIQUE INDEX card_pkey ON public.card USING btree (card_id)`

### `public.chapter_extractions`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `id` | `text` | `NO` | `` |  |
| `user_id` | `text` | `NO` | `` |  |
| `book_id` | `text` | `NO` | `` |  |
| `extractor_type` | `character varying(20)` | `NO` | `` |  |
| `book_extraction_json_local_url` | `text` | `NO` | `` |  |
| `book_extraction_json_oss_url` | `text` | `NO` | `` |  |

约束：
- `CHECK` `2200_20555_1_not_null`：``
- `CHECK` `2200_20555_2_not_null`：``
- `CHECK` `2200_20555_3_not_null`：``
- `CHECK` `2200_20555_4_not_null`：``
- `CHECK` `2200_20555_5_not_null`：``
- `CHECK` `2200_20555_6_not_null`：``
- `FOREIGN KEY` `chapter_extractions_book_id_fkey`：`book_id` → `public.books(book_id)`
- `FOREIGN KEY` `chapter_extractions_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `chapter_extractions_pkey`：`id`

索引：
- `chapter_extractions_pkey`：`CREATE UNIQUE INDEX chapter_extractions_pkey ON public.chapter_extractions USING btree (id)`

### `public.extraction_tasks`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `id` | `bigint` | `NO` | `nextval('extraction_tasks_id_seq'::regclass)` |  |
| `user_id` | `text` | `NO` | `` |  |
| `book_id` | `text` | `NO` | `` |  |
| `task_type` | `text` | `NO` | `` |  |
| `status` | `text` | `NO` | `'pending'::text` |  |
| `progress` | `integer` | `NO` | `0` |  |
| `error_message` | `text` | `YES` | `` |  |
| `created_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `updated_at` | `timestamp with time zone` | `NO` | `now()` |  |

约束：
- `CHECK` `2200_25420_1_not_null`：``
- `CHECK` `2200_25420_2_not_null`：``
- `CHECK` `2200_25420_3_not_null`：``
- `CHECK` `2200_25420_4_not_null`：``
- `CHECK` `2200_25420_5_not_null`：``
- `CHECK` `2200_25420_6_not_null`：``
- `CHECK` `2200_25420_8_not_null`：``
- `CHECK` `2200_25420_9_not_null`：``
- `FOREIGN KEY` `extraction_tasks_book_id_fkey`：`book_id` → `public.books(book_id)`
- `FOREIGN KEY` `extraction_tasks_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `extraction_tasks_pkey`：`id`

索引：
- `extraction_tasks_pkey`：`CREATE UNIQUE INDEX extraction_tasks_pkey ON public.extraction_tasks USING btree (id)`
- `idx_extraction_tasks_book_updated`：`CREATE INDEX idx_extraction_tasks_book_updated ON public.extraction_tasks USING btree (book_id, updated_at DESC)`
- `idx_extraction_tasks_status`：`CREATE INDEX idx_extraction_tasks_status ON public.extraction_tasks USING btree (status)`
- `idx_extraction_tasks_user_updated`：`CREATE INDEX idx_extraction_tasks_user_updated ON public.extraction_tasks USING btree (user_id, updated_at DESC)`

### `public.prompt_config`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `prompt_id` | `text` | `NO` | `` |  |
| `user_id` | `text` | `NO` | `` |  |
| `type` | `text` | `NO` | `` |  |
| `prompt_url` | `text` | `NO` | `` |  |
| `created_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |
| `updated_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |

约束：
- `CHECK` `2200_20572_1_not_null`：``
- `CHECK` `2200_20572_2_not_null`：``
- `CHECK` `2200_20572_3_not_null`：``
- `CHECK` `2200_20572_4_not_null`：``
- `CHECK` `2200_20572_5_not_null`：``
- `CHECK` `2200_20572_6_not_null`：``
- `FOREIGN KEY` `prompt_config_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `prompt_config_pkey`：`prompt_id`

索引：
- `prompt_config_pkey`：`CREATE UNIQUE INDEX prompt_config_pkey ON public.prompt_config USING btree (prompt_id)`

### `public.summary`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `summary_id` | `text` | `NO` | `` |  |
| `book_id` | `text` | `NO` | `` |  |
| `type` | `text` | `NO` | `` |  |
| `name` | `text` | `YES` | `` |  |
| `created_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |
| `updated_at` | `timestamp without time zone` | `NO` | `CURRENT_TIMESTAMP` |  |
| `prompt_id` | `text` | `YES` | `` |  |
| `content_local_url` | `character varying(1024)` | `YES` | `` |  |
| `content_oss_url` | `character varying(1024)` | `YES` | `` |  |

约束：
- `CHECK` `2200_20586_1_not_null`：``
- `CHECK` `2200_20586_3_not_null`：``
- `CHECK` `2200_20586_4_not_null`：``
- `CHECK` `2200_20586_7_not_null`：``
- `CHECK` `2200_20586_8_not_null`：``
- `FOREIGN KEY` `summary_book_id_fkey`：`book_id` → `public.books(book_id)`
- `FOREIGN KEY` `summary_prompt_id_fkey`：`prompt_id` → `public.prompt_config(prompt_id)`
- `PRIMARY KEY` `summary_pkey`：`summary_id`

索引：
- `summary_pkey`：`CREATE UNIQUE INDEX summary_pkey ON public.summary USING btree (summary_id)`

### `public.task_logs`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `id` | `bigint` | `NO` | `nextval('task_logs_id_seq'::regclass)` |  |
| `task_id` | `text` | `YES` | `` |  |
| `user_id` | `text` | `NO` | `` |  |
| `level` | `text` | `NO` | `'info'::text` |  |
| `message` | `text` | `NO` | `` |  |
| `detail_json` | `jsonb` | `YES` | `` |  |
| `created_at` | `timestamp with time zone` | `NO` | `now()` |  |

约束：
- `CHECK` `2200_25446_1_not_null`：``
- `CHECK` `2200_25446_3_not_null`：``
- `CHECK` `2200_25446_4_not_null`：``
- `CHECK` `2200_25446_5_not_null`：``
- `CHECK` `2200_25446_7_not_null`：``
- `FOREIGN KEY` `task_logs_user_id_fkey`：`user_id` → `public.users(user_id)`
- `PRIMARY KEY` `task_logs_pkey`：`id`

索引：
- `idx_task_logs_level`：`CREATE INDEX idx_task_logs_level ON public.task_logs USING btree (level)`
- `idx_task_logs_task_created`：`CREATE INDEX idx_task_logs_task_created ON public.task_logs USING btree (task_id, created_at DESC)`
- `idx_task_logs_user_created`：`CREATE INDEX idx_task_logs_user_created ON public.task_logs USING btree (user_id, created_at DESC)`
- `task_logs_pkey`：`CREATE UNIQUE INDEX task_logs_pkey ON public.task_logs USING btree (id)`

### `public.users`

| 字段 | 类型 | 可为空 | 默认值 | 备注 |
|---|---|---|---|---|
| `user_id` | `text` | `NO` | `gen_prefixed_id('u'::text)` |  |
| `username` | `text` | `NO` | `` |  |
| `email` | `text` | `YES` | `` |  |
| `password_hash` | `text` | `NO` | `` |  |
| `status` | `text` | `YES` | `'active'::text` |  |
| `created_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `updated_at` | `timestamp with time zone` | `NO` | `now()` |  |
| `avatar` | `text` | `YES` | `` |  |
| `prompt` | `text` | `YES` | `` |  |

约束：
- `CHECK` `2200_17875_1_not_null`：``
- `CHECK` `2200_17875_2_not_null`：``
- `CHECK` `2200_17875_4_not_null`：``
- `CHECK` `2200_17875_6_not_null`：``
- `CHECK` `2200_17875_7_not_null`：``
- `CHECK` `users_status_check`：``
- `PRIMARY KEY` `users_pkey`：`user_id`
- `UNIQUE` `users_email_key`：`email`
- `UNIQUE` `users_username_key`：`username`

索引：
- `users_email_key`：`CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email)`
- `users_pkey`：`CREATE UNIQUE INDEX users_pkey ON public.users USING btree (user_id)`
- `users_username_key`：`CREATE UNIQUE INDEX users_username_key ON public.users USING btree (username)`

触发器：
- `trg_users_updated_at`：`BEFORE UPDATE`

## public 函数

### `public.array_to_halfvec(numeric[], integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_halfvec(numeric[], integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_halfvec$function$
```

### `public.array_to_halfvec(integer[], integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_halfvec(integer[], integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_halfvec$function$
```

### `public.array_to_halfvec(real[], integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_halfvec(real[], integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_halfvec$function$
```

### `public.array_to_halfvec(double precision[], integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_halfvec(double precision[], integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_halfvec$function$
```

### `public.array_to_sparsevec(real[], integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_sparsevec(real[], integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_sparsevec$function$
```

### `public.array_to_sparsevec(numeric[], integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_sparsevec(numeric[], integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_sparsevec$function$
```

### `public.array_to_sparsevec(double precision[], integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_sparsevec(double precision[], integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_sparsevec$function$
```

### `public.array_to_sparsevec(integer[], integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.array_to_sparsevec(integer[], integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_sparsevec$function$
```

### `public.array_to_vector(real[], integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.array_to_vector(real[], integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_vector$function$
```

### `public.array_to_vector(numeric[], integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.array_to_vector(numeric[], integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_vector$function$
```

### `public.array_to_vector(double precision[], integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.array_to_vector(double precision[], integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_vector$function$
```

### `public.array_to_vector(integer[], integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.array_to_vector(integer[], integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$array_to_vector$function$
```

### `public.binary_quantize(halfvec)`

返回：`bit`

```sql
CREATE OR REPLACE FUNCTION public.binary_quantize(halfvec)
 RETURNS bit
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_binary_quantize$function$
```

### `public.binary_quantize(vector)`

返回：`bit`

```sql
CREATE OR REPLACE FUNCTION public.binary_quantize(vector)
 RETURNS bit
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$binary_quantize$function$
```

### `public.cosine_distance(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.cosine_distance(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_cosine_distance$function$
```

### `public.cosine_distance(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.cosine_distance(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_cosine_distance$function$
```

### `public.cosine_distance(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.cosine_distance(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$cosine_distance$function$
```

### `public.gen_prefixed_id(prefix text)`

返回：`text`

```sql
CREATE OR REPLACE FUNCTION public.gen_prefixed_id(prefix text)
 RETURNS text
 LANGUAGE sql
AS $function$
  select prefix || '_' || substr(replace(gen_random_uuid()::text, '-', ''), 1, 16);
$function$
```

### `public.halfvec(halfvec, integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec(halfvec, integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec$function$
```

### `public.halfvec_accum(double precision[], halfvec)`

返回：`double precision[]`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_accum(double precision[], halfvec)
 RETURNS double precision[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_accum$function$
```

### `public.halfvec_add(halfvec, halfvec)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_add(halfvec, halfvec)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_add$function$
```

### `public.halfvec_avg(double precision[])`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_avg(double precision[])
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_avg$function$
```

### `public.halfvec_cmp(halfvec, halfvec)`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_cmp(halfvec, halfvec)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_cmp$function$
```

### `public.halfvec_combine(double precision[], double precision[])`

返回：`double precision[]`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_combine(double precision[], double precision[])
 RETURNS double precision[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_combine$function$
```

### `public.halfvec_concat(halfvec, halfvec)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_concat(halfvec, halfvec)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_concat$function$
```

### `public.halfvec_eq(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_eq(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_eq$function$
```

### `public.halfvec_ge(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_ge(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_ge$function$
```

### `public.halfvec_gt(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_gt(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_gt$function$
```

### `public.halfvec_in(cstring, oid, integer)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_in(cstring, oid, integer)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_in$function$
```

### `public.halfvec_l2_squared_distance(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_l2_squared_distance(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_l2_squared_distance$function$
```

### `public.halfvec_le(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_le(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_le$function$
```

### `public.halfvec_lt(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_lt(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_lt$function$
```

### `public.halfvec_mul(halfvec, halfvec)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_mul(halfvec, halfvec)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_mul$function$
```

### `public.halfvec_ne(halfvec, halfvec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_ne(halfvec, halfvec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_ne$function$
```

### `public.halfvec_negative_inner_product(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_negative_inner_product(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_negative_inner_product$function$
```

### `public.halfvec_out(halfvec)`

返回：`cstring`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_out(halfvec)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_out$function$
```

### `public.halfvec_recv(internal, oid, integer)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_recv(internal, oid, integer)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_recv$function$
```

### `public.halfvec_send(halfvec)`

返回：`bytea`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_send(halfvec)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_send$function$
```

### `public.halfvec_spherical_distance(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_spherical_distance(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_spherical_distance$function$
```

### `public.halfvec_sub(halfvec, halfvec)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_sub(halfvec, halfvec)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_sub$function$
```

### `public.halfvec_to_float4(halfvec, integer, boolean)`

返回：`real[]`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_to_float4(halfvec, integer, boolean)
 RETURNS real[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_to_float4$function$
```

### `public.halfvec_to_sparsevec(halfvec, integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_to_sparsevec(halfvec, integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_to_sparsevec$function$
```

### `public.halfvec_to_vector(halfvec, integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_to_vector(halfvec, integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_to_vector$function$
```

### `public.halfvec_typmod_in(cstring[])`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.halfvec_typmod_in(cstring[])
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_typmod_in$function$
```

### `public.hamming_distance(bit, bit)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.hamming_distance(bit, bit)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$hamming_distance$function$
```

### `public.hnsw_bit_support(internal)`

返回：`internal`

```sql
CREATE OR REPLACE FUNCTION public.hnsw_bit_support(internal)
 RETURNS internal
 LANGUAGE c
AS '$libdir/vector', $function$hnsw_bit_support$function$
```

### `public.hnsw_halfvec_support(internal)`

返回：`internal`

```sql
CREATE OR REPLACE FUNCTION public.hnsw_halfvec_support(internal)
 RETURNS internal
 LANGUAGE c
AS '$libdir/vector', $function$hnsw_halfvec_support$function$
```

### `public.hnsw_sparsevec_support(internal)`

返回：`internal`

```sql
CREATE OR REPLACE FUNCTION public.hnsw_sparsevec_support(internal)
 RETURNS internal
 LANGUAGE c
AS '$libdir/vector', $function$hnsw_sparsevec_support$function$
```

### `public.hnswhandler(internal)`

返回：`index_am_handler`

```sql
CREATE OR REPLACE FUNCTION public.hnswhandler(internal)
 RETURNS index_am_handler
 LANGUAGE c
AS '$libdir/vector', $function$hnswhandler$function$
```

### `public.inner_product(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.inner_product(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_inner_product$function$
```

### `public.inner_product(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.inner_product(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_inner_product$function$
```

### `public.inner_product(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.inner_product(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$inner_product$function$
```

### `public.ivfflat_bit_support(internal)`

返回：`internal`

```sql
CREATE OR REPLACE FUNCTION public.ivfflat_bit_support(internal)
 RETURNS internal
 LANGUAGE c
AS '$libdir/vector', $function$ivfflat_bit_support$function$
```

### `public.ivfflat_halfvec_support(internal)`

返回：`internal`

```sql
CREATE OR REPLACE FUNCTION public.ivfflat_halfvec_support(internal)
 RETURNS internal
 LANGUAGE c
AS '$libdir/vector', $function$ivfflat_halfvec_support$function$
```

### `public.ivfflathandler(internal)`

返回：`index_am_handler`

```sql
CREATE OR REPLACE FUNCTION public.ivfflathandler(internal)
 RETURNS index_am_handler
 LANGUAGE c
AS '$libdir/vector', $function$ivfflathandler$function$
```

### `public.jaccard_distance(bit, bit)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.jaccard_distance(bit, bit)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$jaccard_distance$function$
```

### `public.l1_distance(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l1_distance(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_l1_distance$function$
```

### `public.l1_distance(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l1_distance(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_l1_distance$function$
```

### `public.l1_distance(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l1_distance(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$l1_distance$function$
```

### `public.l2_distance(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l2_distance(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_l2_distance$function$
```

### `public.l2_distance(halfvec, halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l2_distance(halfvec, halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_l2_distance$function$
```

### `public.l2_distance(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l2_distance(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$l2_distance$function$
```

### `public.l2_norm(halfvec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l2_norm(halfvec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_l2_norm$function$
```

### `public.l2_norm(sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.l2_norm(sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_l2_norm$function$
```

### `public.l2_normalize(sparsevec)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.l2_normalize(sparsevec)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_l2_normalize$function$
```

### `public.l2_normalize(halfvec)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.l2_normalize(halfvec)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_l2_normalize$function$
```

### `public.l2_normalize(vector)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.l2_normalize(vector)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$l2_normalize$function$
```

### `public.set_updated_at()`

返回：`trigger`

```sql
CREATE OR REPLACE FUNCTION public.set_updated_at()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
  new.updated_at = now();
  return new;
end;
$function$
```

### `public.sparsevec(sparsevec, integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec(sparsevec, integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec$function$
```

### `public.sparsevec_cmp(sparsevec, sparsevec)`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_cmp(sparsevec, sparsevec)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_cmp$function$
```

### `public.sparsevec_eq(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_eq(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_eq$function$
```

### `public.sparsevec_ge(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_ge(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_ge$function$
```

### `public.sparsevec_gt(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_gt(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_gt$function$
```

### `public.sparsevec_in(cstring, oid, integer)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_in(cstring, oid, integer)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_in$function$
```

### `public.sparsevec_l2_squared_distance(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_l2_squared_distance(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_l2_squared_distance$function$
```

### `public.sparsevec_le(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_le(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_le$function$
```

### `public.sparsevec_lt(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_lt(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_lt$function$
```

### `public.sparsevec_ne(sparsevec, sparsevec)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_ne(sparsevec, sparsevec)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_ne$function$
```

### `public.sparsevec_negative_inner_product(sparsevec, sparsevec)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_negative_inner_product(sparsevec, sparsevec)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_negative_inner_product$function$
```

### `public.sparsevec_out(sparsevec)`

返回：`cstring`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_out(sparsevec)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_out$function$
```

### `public.sparsevec_recv(internal, oid, integer)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_recv(internal, oid, integer)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_recv$function$
```

### `public.sparsevec_send(sparsevec)`

返回：`bytea`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_send(sparsevec)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_send$function$
```

### `public.sparsevec_to_halfvec(sparsevec, integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_to_halfvec(sparsevec, integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_to_halfvec$function$
```

### `public.sparsevec_to_vector(sparsevec, integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_to_vector(sparsevec, integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_to_vector$function$
```

### `public.sparsevec_typmod_in(cstring[])`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.sparsevec_typmod_in(cstring[])
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$sparsevec_typmod_in$function$
```

### `public.subvector(halfvec, integer, integer)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.subvector(halfvec, integer, integer)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_subvector$function$
```

### `public.subvector(vector, integer, integer)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.subvector(vector, integer, integer)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$subvector$function$
```

### `public.vector(vector, integer, boolean)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector(vector, integer, boolean)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector$function$
```

### `public.vector_accum(double precision[], vector)`

返回：`double precision[]`

```sql
CREATE OR REPLACE FUNCTION public.vector_accum(double precision[], vector)
 RETURNS double precision[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_accum$function$
```

### `public.vector_add(vector, vector)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_add(vector, vector)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_add$function$
```

### `public.vector_avg(double precision[])`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_avg(double precision[])
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_avg$function$
```

### `public.vector_cmp(vector, vector)`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.vector_cmp(vector, vector)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_cmp$function$
```

### `public.vector_combine(double precision[], double precision[])`

返回：`double precision[]`

```sql
CREATE OR REPLACE FUNCTION public.vector_combine(double precision[], double precision[])
 RETURNS double precision[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_combine$function$
```

### `public.vector_concat(vector, vector)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_concat(vector, vector)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_concat$function$
```

### `public.vector_dims(halfvec)`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.vector_dims(halfvec)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$halfvec_vector_dims$function$
```

### `public.vector_dims(vector)`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.vector_dims(vector)
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_dims$function$
```

### `public.vector_eq(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_eq(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_eq$function$
```

### `public.vector_ge(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_ge(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_ge$function$
```

### `public.vector_gt(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_gt(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_gt$function$
```

### `public.vector_in(cstring, oid, integer)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_in(cstring, oid, integer)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_in$function$
```

### `public.vector_l2_squared_distance(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.vector_l2_squared_distance(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_l2_squared_distance$function$
```

### `public.vector_le(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_le(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_le$function$
```

### `public.vector_lt(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_lt(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_lt$function$
```

### `public.vector_mul(vector, vector)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_mul(vector, vector)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_mul$function$
```

### `public.vector_ne(vector, vector)`

返回：`boolean`

```sql
CREATE OR REPLACE FUNCTION public.vector_ne(vector, vector)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_ne$function$
```

### `public.vector_negative_inner_product(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.vector_negative_inner_product(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_negative_inner_product$function$
```

### `public.vector_norm(vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.vector_norm(vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_norm$function$
```

### `public.vector_out(vector)`

返回：`cstring`

```sql
CREATE OR REPLACE FUNCTION public.vector_out(vector)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_out$function$
```

### `public.vector_recv(internal, oid, integer)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_recv(internal, oid, integer)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_recv$function$
```

### `public.vector_send(vector)`

返回：`bytea`

```sql
CREATE OR REPLACE FUNCTION public.vector_send(vector)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_send$function$
```

### `public.vector_spherical_distance(vector, vector)`

返回：`double precision`

```sql
CREATE OR REPLACE FUNCTION public.vector_spherical_distance(vector, vector)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_spherical_distance$function$
```

### `public.vector_sub(vector, vector)`

返回：`vector`

```sql
CREATE OR REPLACE FUNCTION public.vector_sub(vector, vector)
 RETURNS vector
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_sub$function$
```

### `public.vector_to_float4(vector, integer, boolean)`

返回：`real[]`

```sql
CREATE OR REPLACE FUNCTION public.vector_to_float4(vector, integer, boolean)
 RETURNS real[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_to_float4$function$
```

### `public.vector_to_halfvec(vector, integer, boolean)`

返回：`halfvec`

```sql
CREATE OR REPLACE FUNCTION public.vector_to_halfvec(vector, integer, boolean)
 RETURNS halfvec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_to_halfvec$function$
```

### `public.vector_to_sparsevec(vector, integer, boolean)`

返回：`sparsevec`

```sql
CREATE OR REPLACE FUNCTION public.vector_to_sparsevec(vector, integer, boolean)
 RETURNS sparsevec
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_to_sparsevec$function$
```

### `public.vector_typmod_in(cstring[])`

返回：`integer`

```sql
CREATE OR REPLACE FUNCTION public.vector_typmod_in(cstring[])
 RETURNS integer
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/vector', $function$vector_typmod_in$function$
```
