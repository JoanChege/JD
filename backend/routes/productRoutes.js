const express = require('express');
const Product = require('../models/Product');

const router = express.Router();

// Get all products (with optional filtering by category and subcategory)
router.get('/', async (req, res) => {
    const { category, subcategory } = req.query;
    const query = {};

  // Add category and subcategory to the query if provided
    if (category) query.category = category;
    if (subcategory) query.subcategory = subcategory;

    try {
        const products = await Product.find(query);
        res.json(products);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Add a new product
router.post('/', async (req, res) => {
    const product = new Product({
        name: req.body.name,
        price: req.body.price,
        description: req.body.description,
        image: req.body.image,
        category: req.body.category, // Include category
        subcategory: req.body.subcategory, // Include subcategory
    });

    try {
        const newProduct = await product.save();
        res.status(201).json(newProduct);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Get a single product by ID
router.get('/:id', async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);
        if (!product) {
        return res.status(404).json({ message: 'Product not found' });
        }
        res.json(product);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Update a product by ID
router.put('/:id', async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);
        if (!product) {
        return res.status(404).json({ message: 'Product not found' });
        }

    // Update fields if they are provided in the request body
    if (req.body.name) product.name = req.body.name;
    if (req.body.price) product.price = req.body.price;
    if (req.body.description) product.description = req.body.description;
    if (req.body.image) product.image = req.body.image;
    if (req.body.category) product.category = req.body.category;
    if (req.body.subcategory) product.subcategory = req.body.subcategory;

    const updatedProduct = await product.save();
    res.json(updatedProduct);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Delete a product by ID
router.delete('/:id', async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);
        if (!product) {
        return res.status(404).json({ message: 'Product not found' });
        }

        await product.remove();
        res.json({ message: 'Product deleted' });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;