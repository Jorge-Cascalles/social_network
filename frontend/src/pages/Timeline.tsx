import React, { useState, useEffect } from 'react';
import { Card, Form, Button, InputGroup, ListGroup } from 'react-bootstrap';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface Post {
  id: string;
  titulo: string;
  conteudo: string;
  imagem_url?: string;
  data_criacao: string;
  autor: {
    email: string;
    nome: string;
    foto?: string;
  };
}

const Timeline: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [newPost, setNewPost] = useState({ titulo: '', conteudo: '', imagem_url: '' });
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const { data } = await axios.get<Post[]>('http://localhost:8000/api/timeline');
      setPosts(data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/posts', newPost);
      setNewPost({ titulo: '', conteudo: '', imagem_url: '' });
      fetchPosts();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Card className="mb-4">
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Title</Form.Label>
              <Form.Control
                type="text"
                value={newPost.titulo}
                onChange={(e) => setNewPost({ ...newPost, titulo: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Content</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={newPost.conteudo}
                onChange={(e) => setNewPost({ ...newPost, conteudo: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Image URL (optional)</Form.Label>
              <Form.Control
                type="url"
                value={newPost.imagem_url}
                onChange={(e) => setNewPost({ ...newPost, imagem_url: e.target.value })}
              />
            </Form.Group>
            <Button type="submit">Create Post</Button>
          </Form>
        </Card.Body>
      </Card>

      <ListGroup>
        {posts.map((post) => (
          <ListGroup.Item key={post.id}>
            <Card>
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  {post.autor.foto && (
                    <img
                      src={post.autor.foto}
                      alt={post.autor.nome}
                      style={{ width: '40px', height: '40px', borderRadius: '50%', marginRight: '10px' }}
                    />
                  )}
                  <div>
                    <Card.Title>{post.titulo}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                      Posted by {post.autor.nome} on {new Date(post.data_criacao).toLocaleDateString()}
                    </Card.Subtitle>
                  </div>
                </div>
                <Card.Text>{post.conteudo}</Card.Text>
                {post.imagem_url && (
                  <img
                    src={post.imagem_url}
                    alt="Post"
                    style={{ maxWidth: '100%', maxHeight: '400px', objectFit: 'contain' }}
                  />
                )}
              </Card.Body>
            </Card>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
};

export default Timeline; 