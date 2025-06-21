import { Link } from 'react-router-dom';
import logo from '../../assets/logo.svg';
import styles from './Header.module.css';
import { useEffect, useState } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { authStore } from '../../stores/AuthStore';

const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    console.log(authStore.isAuth);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    useEffect(() => {

    }, [authStore.isAuth])

    return (
        <header className={styles.Header}>
            <nav className={styles.wrapper}>
                <Link to='/' className={styles.logoLink}>
                    <img src={logo} alt="Логотип" />
                </Link>
                
                <div className={`${styles.navLinks} ${isMenuOpen ? styles.active : ''}`}>
                    <Link to='reports' className={styles.link} onClick={() => setIsMenuOpen(false)}>Объявления</Link>
                    <Link to={authStore.isAuth ? '/post/reports' : '/login'} className={styles.link} onClick={() => setIsMenuOpen(false)}>Разместить объявление</Link>
                    { authStore.user?.role == 'admin' && <Link to='/blogs' className={styles.link} onClick={() => setIsMenuOpen(false)}>Статьи</Link>}
                    { !authStore.isAuth ? 
                    <Link to='/login' className={styles.link}>Вход</Link> : 
                    <Link to='/profile' className={styles.link}>Профиль</Link>
                    }
                    
                </div>
                
                <div className={styles.mobileMenuButton} onClick={toggleMenu}>
                    {isMenuOpen ? <FaTimes /> : <FaBars />}
                </div>
            </nav>
        </header>
    );
}

export default Header;