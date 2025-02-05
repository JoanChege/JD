const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  description: { type: String, required: true },
  image: { type: String, required: true },
  category: {
    type: String,
    required: true,
    enum: ['Dresses', 'Shoes', 'Coats', 'Panties', 'Accessories', 'Suits', 'Blouses'], // Main categories
  },
  subcategory: {
    type: String,
    required: function () {
      // Subcategory is required only for certain categories
      return this.category === 'Dresses' || this.category === 'Coats' || this.category === 'Suits';
    },
    enum: {
      values: [
        // Subcategories for Dresses
        'Formal Dresses', 'Casual Dresses', 'Shirt Dresses',
        // Subcategories for Coats
        'Long Coats', 'Short Coats',
        // Subcategories for Suits
        'Skirt Suits', 'Dress Suits', 'Pant Suits',
      ],
      message: '{VALUE} is not a valid subcategory for this category',
    },
  },
});

module.exports = mongoose.model('Product', productSchema);