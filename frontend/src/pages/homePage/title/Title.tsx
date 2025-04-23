import styles from './Title.module.css'
import { Link } from 'react-router-dom'

const Title = () => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.contentWrapper}>
                <h1 className={styles.title}>Система поиска домашних животных</h1>
                <div className={styles.subtitleWrapper}>
                    <p className={styles.subTitle}>Что случилось?</p>
                    <div className={styles.links}>
                        <Link to='reports/found' className={styles.lost}>Потерял питомца</Link>
                        <Link to='reports/lost' className={styles.found}>Нашел питомца</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
 
export default Title;