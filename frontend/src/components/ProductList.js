import React, { useEffect, useState } from 'react';
import { productAPI } from '../services/api';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await productAPI.get('/');
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading products...</div>;

  return (
    <div className="product-grid">
      <h2>🔥 Featured Products</h2>
      <div className="grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <p className="price">₹{product.price}</p>
            <button className="btn-primary">Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
