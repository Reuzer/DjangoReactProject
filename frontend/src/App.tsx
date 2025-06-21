import { BrowserRouter, Route, Routes } from 'react-router'
import './App.css'
import { routesConfig } from './config/routes'
import Header from './components/header/Header'
import Footer from './components/footer/Footer'
import { observer } from 'mobx-react-lite'
import { useEffect } from 'react'
import { authStore } from './stores/AuthStore'





const App = observer(() => {

  useEffect(() => {
    // Проверяем токен при загрузке приложения
    if (authStore.tokens?.access && !authStore.isAuth) {
      authStore.refreshToken();
    }
  }, []);

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
})

export default App
