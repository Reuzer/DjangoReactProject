import { Link } from 'react-router-dom';
import logo from '../../assets/logo.svg'
import styles from './Header.module.css'

const Header = () => {
    console.log('render')
    return (
        <header className={styles.Header}>
            <nav className={styles.wrapper}>
                <Link to='/' className={styles.link}><img src={logo} alt="" /></Link>
                <Link to='reports' className={styles.link}>Объявления</Link>
                <Link to='reports/post' className={styles.link}>Разместить объявление</Link>
            </nav>
        </header>
    );
}
 
export default Header;