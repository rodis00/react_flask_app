import './App.css';
import { useState, useEffect } from 'react';
import ArticleList from './components/ArticleList';
import Form from './components/Form';

function App() {

  const [articles, setArticles] = useState([])
  const [editedArticle, setEditedArticle] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:5000/get', {
      'method': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(resp => resp.json())
      .then(resp => setArticles(resp))
      .catch(error => console.log(error))

  }, [])

  const editArticle = (article) => {
    setEditedArticle(article)
  }

  const updatedData = (article) => {
    const new_article = articles.map(my_article => {
      if (my_article.id === article.id)
        return article
      return my_article
    })
    setArticles(new_article)
  }

  const openForm = () => {
    setEditedArticle({ title: '', body: '' })
  }

  const insertArticle = (article) => {
    const new_article = [...articles, article]
    setArticles(new_article)
  }

  const deleteArticle = (article) => {
    const new_article = articles.filter(myarticle => {
      if (myarticle.id === article.id)
        return false;
      return true
    })
    setArticles(new_article)
  }

  return (
    <div className="App">
      <div className='row'>
        <div className='col'>
          <h1>Flask and React App</h1>

        </div>
        <div className='col'>
          <button className='btn btn-success' onClick={openForm}>InsertArticle</button>
        </div>
      </div>
      <br />
      <br />

      <ArticleList articles={articles} editArticle={editArticle} deleteArticle={deleteArticle} />

      {editedArticle ? <Form article={editedArticle} updatedData={updatedData} insertArticle={insertArticle} /> : null}

    </div>
  );
}

export default App;
