-- db/init_products.sql

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price INTEGER NOT NULL
);

INSERT INTO products (name, price) VALUES
  ('Sourdough', 500),
  ('Croissant', 200),
  ('Baguette', 150)
ON CONFLICT DO NOTHING;
