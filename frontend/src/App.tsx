import { BrowserRouter, Route, Routes } from 'react-router'
import './App.css'
import { routesConfig } from './config/routes'
import Header from './components/header/Header'
import Footer from './components/footer/Footer'




function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        {routesConfig.map(item => 
          <Route key={item.path} path={item.path} element={item.element} />
        )}
      </Routes>
      <Footer />
    </BrowserRouter>
  )
}

export default App
