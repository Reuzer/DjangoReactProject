import { useEffect, useState } from "react";
import ServiceApi from "../../../api/serviceAPI";
import { Review } from "../../../api/types";
import styles from './Reviews.module.css'
import Img from "../../../components/Img/Img";
import alter from '../../../assets/alter.svg'
import Stars from "../../../components/stars/Stars";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

const Reviews = () => {
    const [reviews, setReviews] = useState<Review[]>([]);
    const [avgRating, setAvgRating] = useState<number>(0)
    const [currentIndex, setCurrentIndex] = useState(0);
    const [visibleCount] = useState(4);

    const fetching = async () => {
        const reviewResponse = await ServiceApi.getReviews();
        const avgRatingResponse = await ServiceApi.getAvgReviewRating();
        setReviews(reviewResponse.data);
        setAvgRating(avgRatingResponse.data.avg_rating);
    }

    useEffect(() => {
        fetching();
    }, []);

    const nextSlide = () => {
        setCurrentIndex(prevIndex => 
            prevIndex + 1 <= reviews.length - visibleCount ? prevIndex + 1 : 0
        );
    };

    const prevSlide = () => {
        setCurrentIndex(prevIndex => 
            prevIndex - 1 >= 0 ? prevIndex - 1 : reviews.length - visibleCount
        );
    };

    const visibleReviews = reviews.slice(currentIndex, currentIndex + visibleCount);

    return (
        <div className={styles.wrapper}>
            <h2 className={styles.title}>Отзывы</h2>
            <div className={styles.sliderContainer}>
                <button 
                    onClick={prevSlide} 
                    className={styles.navButton}
                    disabled={reviews.length <= visibleCount}
                >
                    <FaChevronLeft />
                </button>
                
                <ul className={styles.container}>
                    {visibleReviews.map(item =>
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
                
                <button 
                    onClick={nextSlide} 
                    className={styles.navButton}
                    disabled={reviews.length <= visibleCount}
                >
                    <FaChevronRight />
                </button>
            </div>
            <p className={styles.avg_rating}>Средний рейтинг: {avgRating}</p>
        </div>
    );
}
 
export default Reviews;