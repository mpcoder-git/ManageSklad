PGDMP      -            	    |            managesklad    17rc1    17rc1 '    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16387    managesklad    DATABASE        CREATE DATABASE managesklad WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE managesklad;
                     admin    false            �            1259    16481    orders    TABLE     �   CREATE TABLE public.orders (
    id integer NOT NULL,
    datecreate timestamp without time zone NOT NULL,
    status_id integer
);
    DROP TABLE public.orders;
       public         heap r       admin    false            �            1259    16480    orders_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.orders_id_seq;
       public               admin    false    222            �           0    0    orders_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;
          public               admin    false    221            �            1259    16494    ordersitems    TABLE     �   CREATE TABLE public.ordersitems (
    id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity double precision
);
    DROP TABLE public.ordersitems;
       public         heap r       admin    false            �            1259    16493    ordersitems_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ordersitems_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.ordersitems_id_seq;
       public               admin    false    224            �           0    0    ordersitems_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.ordersitems_id_seq OWNED BY public.ordersitems.id;
          public               admin    false    223            �            1259    16461    products    TABLE     �   CREATE TABLE public.products (
    id integer NOT NULL,
    prodname character varying NOT NULL,
    description character varying,
    price double precision NOT NULL,
    stock double precision NOT NULL
);
    DROP TABLE public.products;
       public         heap r       admin    false            �            1259    16460    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public               admin    false    218            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public               admin    false    217            �            1259    16471    statuses    TABLE     e   CREATE TABLE public.statuses (
    id integer NOT NULL,
    statusname character varying NOT NULL
);
    DROP TABLE public.statuses;
       public         heap r       admin    false            �            1259    16470    statuses_id_seq    SEQUENCE     �   CREATE SEQUENCE public.statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.statuses_id_seq;
       public               admin    false    220            �           0    0    statuses_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.statuses_id_seq OWNED BY public.statuses.id;
          public               admin    false    219            2           2604    16484 	   orders id    DEFAULT     f   ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);
 8   ALTER TABLE public.orders ALTER COLUMN id DROP DEFAULT;
       public               admin    false    221    222    222            3           2604    16497    ordersitems id    DEFAULT     p   ALTER TABLE ONLY public.ordersitems ALTER COLUMN id SET DEFAULT nextval('public.ordersitems_id_seq'::regclass);
 =   ALTER TABLE public.ordersitems ALTER COLUMN id DROP DEFAULT;
       public               admin    false    223    224    224            0           2604    16464    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public               admin    false    217    218    218            1           2604    16474    statuses id    DEFAULT     j   ALTER TABLE ONLY public.statuses ALTER COLUMN id SET DEFAULT nextval('public.statuses_id_seq'::regclass);
 :   ALTER TABLE public.statuses ALTER COLUMN id DROP DEFAULT;
       public               admin    false    219    220    220            �          0    16481    orders 
   TABLE DATA           ;   COPY public.orders (id, datecreate, status_id) FROM stdin;
    public               admin    false    222   �)       �          0    16494    ordersitems 
   TABLE DATA           I   COPY public.ordersitems (id, order_id, product_id, quantity) FROM stdin;
    public               admin    false    224   �)       �          0    16461    products 
   TABLE DATA           K   COPY public.products (id, prodname, description, price, stock) FROM stdin;
    public               admin    false    218   �)       �          0    16471    statuses 
   TABLE DATA           2   COPY public.statuses (id, statusname) FROM stdin;
    public               admin    false    220   '*       �           0    0    orders_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.orders_id_seq', 1, false);
          public               admin    false    221            �           0    0    ordersitems_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.ordersitems_id_seq', 1, false);
          public               admin    false    223            �           0    0    products_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.products_id_seq', 2, true);
          public               admin    false    217            �           0    0    statuses_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.statuses_id_seq', 1, false);
          public               admin    false    219            <           2606    16486    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 admin    false    222            ?           2606    16499    ordersitems ordersitems_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.ordersitems
    ADD CONSTRAINT ordersitems_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.ordersitems DROP CONSTRAINT ordersitems_pkey;
       public                 admin    false    224            6           2606    16468    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 admin    false    218            9           2606    16478    statuses statuses_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.statuses DROP CONSTRAINT statuses_pkey;
       public                 admin    false    220            :           1259    16492    ix_orders_id    INDEX     =   CREATE INDEX ix_orders_id ON public.orders USING btree (id);
     DROP INDEX public.ix_orders_id;
       public                 admin    false    222            =           1259    16510    ix_ordersitems_id    INDEX     G   CREATE INDEX ix_ordersitems_id ON public.ordersitems USING btree (id);
 %   DROP INDEX public.ix_ordersitems_id;
       public                 admin    false    224            4           1259    16469    ix_products_id    INDEX     A   CREATE INDEX ix_products_id ON public.products USING btree (id);
 "   DROP INDEX public.ix_products_id;
       public                 admin    false    218            7           1259    16479    ix_statuses_id    INDEX     A   CREATE INDEX ix_statuses_id ON public.statuses USING btree (id);
 "   DROP INDEX public.ix_statuses_id;
       public                 admin    false    220            @           2606    16487    orders orders_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);
 F   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_status_id_fkey;
       public               admin    false    4665    222    220            A           2606    16500 %   ordersitems ordersitems_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.ordersitems
    ADD CONSTRAINT ordersitems_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);
 O   ALTER TABLE ONLY public.ordersitems DROP CONSTRAINT ordersitems_order_id_fkey;
       public               admin    false    224    4668    222            B           2606    16505 '   ordersitems ordersitems_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.ordersitems
    ADD CONSTRAINT ordersitems_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);
 Q   ALTER TABLE ONLY public.ordersitems DROP CONSTRAINT ordersitems_product_id_fkey;
       public               admin    false    4662    224    218            �      x������ � �      �      x������ � �      �   7   x�3�(�O)M.Q��tI-N.�,(����9͹���F(�F���&\1z\\\ ���      �   A   x�3估I�����]l���b���[��8��&����.쾰��^.c�[�@	�`� �9)C     