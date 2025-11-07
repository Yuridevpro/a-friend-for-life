-- Schema do Banco de Dados SQLite --

CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE TABLE "divulgar_pet_fotos_secundarias" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_id" bigint NOT NULL REFERENCES "divulgar_pet" ("id") DEFERRABLE INITIALLY DEFERRED, "petimage_id" bigint NOT NULL REFERENCES "divulgar_petimage" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

CREATE TABLE "divulgar_pet" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(1) NOT NULL, "especie" varchar(10) NOT NULL, "sexo" varchar(10) NOT NULL, "tamanho" varchar(10) NOT NULL, "cuidados" text NOT NULL CHECK ((JSON_VALID("cuidados") OR "cuidados" IS NULL)), "vive_bem_em" text NOT NULL CHECK ((JSON_VALID("vive_bem_em") OR "vive_bem_em" IS NULL)), "temperamento" text NOT NULL CHECK ((JSON_VALID("temperamento") OR "temperamento" IS NULL)), "sociavel_com" text NOT NULL CHECK ((JSON_VALID("sociavel_com") OR "sociavel_com" IS NULL)), "historia_pet" text NOT NULL, "nome_pet" varchar(10) NOT NULL, "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "telefone" varchar(20) NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "foto_principal" varchar(100) NULL);

CREATE TABLE "divulgar_petimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_id" bigint NOT NULL REFERENCES "divulgar_pet" ("id") DEFERRABLE INITIALLY DEFERRED, "image" varchar(100) NOT NULL);

CREATE TABLE "pagina_inicio_depoimento" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome" varchar(100) NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "mensagem" text NOT NULL, "data_criacao" datetime NOT NULL, "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "sobrenome" varchar(100) NOT NULL);

CREATE TABLE "perfil_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "telefone" varchar(15) NOT NULL, "nome" varchar(100) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "email" varchar(100) NOT NULL, "cidade_nome" varchar(100) NOT NULL, "estado_id" integer NULL, "estado_nome" varchar(100) NOT NULL, "sobrenome" varchar(100) NOT NULL, "foto_perfil" varchar(100) NULL);

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE TABLE "usuarios_ativacao" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "confirmation_token" varchar(32) NOT NULL, "confirmation_token_expiration" datetime NULL, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "usuarios_resetsenha" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "reset_token" varchar(255) NOT NULL, "created_at" datetime NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

