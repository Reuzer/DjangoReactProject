import { useState } from "react";
import { authStore } from "../../stores/AuthStore";
import styles from './Login.module.css';
import { useNavigate } from "react-router";
import { Link } from "react-router-dom";

const Login = () => {

    const navigate = useNavigate();
    
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    async function handleSubmit() {
        if(!username.length) {
            throw new Error('Пароль должен содержать хотя бы несколько символов')
        } else if (!password.length) {
            throw new Error('Пароль должен содержать несколько символов')
        }

        await authStore.login(username, password);
        console.log(authStore.error);
        navigate('/');
    }

    console.log(authStore.isAuth)

    return (
        <div className={styles.wrapper}>
            <h1 className={styles.title}>Вход</h1>
            <form noValidate className={styles.form}>
                <label htmlFor="username">Введите логин</label>
                    <input 
                    type="text" 
                    name="username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    />
                <label htmlFor="password">Введите пароль</label>
                    <input 
                    type="password"  
                    name="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    />
                <button 
                className={styles.submitBtn}
                type="button"
                onClick={handleSubmit}
                >Войти</button>
            </form>
            <p className={styles.text}>Нет аккаунта?</p>
            <Link className={styles.link} to='/register'>Регистрация</Link>
        </div>
    );
}
 
export default Login;