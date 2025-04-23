import styles from './Footer.module.css'
import { Link } from 'react-router-dom';
import logo from '../../assets/logo.svg'

const Footer = () => {
    return (
        <>
            <footer className={styles.Footer}>
                <nav className={styles.navbar}>
                    <div className={styles.link_wrapper}>
                        <Link to='/' className={styles.link}><img src={logo} alt="" /></Link>
                        <Link to='reports' className={styles.link}>Объявления</Link>
                        <Link to='reports/post' className={styles.link}>Разместить объявление</Link>
                    </div>
                    <a href="" className={styles.vk}>Вконтакте</a>
                </nav>
                <div className={styles.line}></div>
                <div className={styles.info_wrapper}>
                    <p className={styles.policy}>Политика конфиденцианости</p>
                    <p className={styles.condition}>Условия пользования</p>
                </div>
            </footer>
        </>
    );
}
 
export default Footer;