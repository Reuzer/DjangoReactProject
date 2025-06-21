import styles from './Profile.module.css';
import { authStore } from '../../stores/AuthStore';
import { useNavigate } from 'react-router';
import { useEffect, useState } from 'react';
import ServiceApi from '../../api/serviceAPI';
import { PetReport } from '../../api/types';
import ReportItem from '../reports/reportItem/ReportItem';

const Profile = () => {

    const [userReports, setUserReports] = useState<PetReport[]>();

    const navigate = useNavigate();

    async function handleExit () {
        await authStore.logout();
        navigate('/');
        location.reload();
    }

    const fetching = async () => {
        const responseData = await ServiceApi.getUserReports();
        setUserReports(responseData.data);
    }

    useEffect(() => {
        fetching();
    }, [])

    async function handleDelete() {
        await ServiceApi.deleteReport(userReports![0].id);
        location.reload();
        window.scroll(0, 0)
    }

    return (
        <div className={styles.wrapper}>
            <aside className={styles.aside}>
                <p className={styles.info}>Фамилия: {authStore.user?.last_name}</p>
                <p className={styles.info}>Имя: {authStore.user?.first_name}</p>
                <p className={styles.info}>Телефон: {authStore.user?.phone}</p>
                <p className={styles.info}>Почта: {authStore.user?.email}</p>
                <button 
                className={styles.exitBtn}
                onClick={handleExit}
                >Выйти</button>
            </aside>
            <div className={styles.actionWrapper}>
                <h1 className={styles.title}>Ваше Объявление: </h1>
                {userReports?.map(item => 
                    <ReportItem report={item}/>
                )}

                
            </div>
        </div>
    );
}
 
export default Profile;