import styles from './About.module.css';
import heart from '../../../assets/HomePage/About/heart.svg';
import bell from '../../../assets/HomePage/About/bell.svg';
import person from '../../../assets/HomePage/About/person.svg';
import building from '../../../assets/HomePage/About/building.svg';

const About = () => {
    return (
        <div className={styles.wrapper}>
            <h2 className={styles.title}>О нас</h2>
            <ul className={styles.contentWrapper}>
                <li className={styles.contentElement}>
                    <img src={heart} alt="Иконка сердца" className={styles.icon} />
                    <p className={styles.text}>Помогли n-людям</p>
                </li>
                <li className={styles.contentElement}>
                    <img src={bell} alt="Иконка колокольчика" className={styles.icon} />
                    <p className={styles.text}>Уведомления о нахождении</p>
                </li>
                <li className={styles.contentElement}>
                    <img src={person} alt="Иконка человека" className={styles.icon} />
                    <p className={styles.text}>Быстрая поддержка</p>
                </li>
                <li className={styles.contentElement}>
                    <img src={building} alt="Иконка здания" className={styles.icon} />
                    <p className={styles.text}>Сотрудничество с ветклиниками</p>
                </li>
            </ul>
        </div>
    );
}

export default About;