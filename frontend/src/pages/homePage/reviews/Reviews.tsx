import { useEffect, useState } from "react";
import ServiceApi from "../../../api/serviceAPI";
import { Review } from "../../../api/types";
import styles from './Reviews.module.css'
import Img from "../../../components/Img/Img";
import alter from '../../../assets/alter.svg'
import Stars from "../../../components/stars/Stars";

const Reviews = () => {
    
    const [reviews, setReviews] = useState<Review[]>([]);

    const fetching = async () => {
        const data = await ServiceApi.getReviews();
        setReviews(data.data.slice(0,4));
    }

    useEffect(()=>{
        fetching();
    }, [])

    return (
        <div className={styles.wrapper}>
            <h2 className={styles.title}>Отзывы</h2>
            <ul className={styles.container}>
                {reviews.map(item =>
                    <li key={item.id} className={styles.container__element}>
                        <Img 
                        className={styles.photo}
                        photo={item.photo}
                        altPhoto={alter}
                        />
                        <p className={styles.name}>{[item.user_id.last_name, item.user_id.first_name].join(' ')}</p>
                        <p className={styles.description}>{item.text}</p>
                        <Stars rating={item.rating} className={styles.bar}/>
                    </li>
                )}
            </ul>
        </div>
    );
}
 
export default Reviews;