import { FC, useEffect, useMemo, useState } from "react";
import { PetReport } from "../../../api/types"
import styles from './ReportList.module.css'
import ReportItem from "../reportItem/ReportItem";
import ServiceApi from "../../../api/serviceAPI";
import { useLocation, useNavigate } from "react-router-dom";

interface Props {
    reports: PetReport[];
    setReports: (arr: PetReport[]) => void;
}
 
const ReportList: FC<Props> = ({reports, setReports}) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilter, setSelectedFilter] = useState('all'); // По умолчанию "без фильтров"
    const [currReports, setCurrReports] = useState<PetReport[]>(reports);
    const [isLoading, setIsLoading] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();

    // При изменении reports в пропсах обновляем currReports
    useEffect(() => {
        if (selectedFilter === 'all') {
            setCurrReports(reports);
        }
    }, [reports]);

    // Обработчик фильтрации
    const handleFilter = (filter: string) => {
        setSelectedFilter(filter);
        
        if (filter === 'all') {
            // Сбрасываем фильтры - показываем все отчеты
            setCurrReports(reports);
            navigate(location.pathname, { replace: true });
            return;
        }

        setIsLoading(true);
        
        const filterParams: any = {};
        
        if (filter === 'cat') {
            filterParams.pet_type = 2; // ID для кошек
        } else if (filter === 'dog') {
            filterParams.pet_type = 1; // ID для собак
        } else if (filter === 'found') {
            filterParams.report_type = 'found';
        } else if (filter === 'lost') {
            filterParams.report_type = 'lost';
        }

        // Загружаем отфильтрованные данные
        ServiceApi.getFilteredReports(filterParams)
            .then(response => {
                if(response.status === 200) {
                    setCurrReports(response.data);
                }
            })
            .catch(error => {
                console.error('Error fetching filtered reports:', error);
                // В случае ошибки показываем оригинальные reports
                setCurrReports(reports);
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    // Обработчик поиска (на фронтенде)
    const handleSearch = () => {
        if (!searchQuery) {
            // Если поисковой запрос пуст, возвращаем либо отфильтрованные данные, либо все
            if (selectedFilter === 'all') {
                setCurrReports(reports);
            } else {
                handleFilter(selectedFilter);
            }
            return;
        }
        
        // Фильтруем текущий список (либо все reports, либо уже отфильтрованные)
        const sourceList = selectedFilter === 'all' ? reports : currReports;
        const filtered = sourceList.filter(report => 
            report.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            report.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            report.special_marks.toLowerCase().includes(searchQuery.toLowerCase()) ||
            report.location.toLowerCase().includes(searchQuery.toLowerCase())
        );
        
        setCurrReports(filtered);
    };

    // Debounce для поиска
    useEffect(() => {
        const timer = setTimeout(() => {
            handleSearch();
        }, 500);
        
        return () => clearTimeout(timer);
    }, [searchQuery]);

    return (
        <div className={styles.wrapper}>
            <div className={styles.ui_wrapper}>
                <input 
                    type="text"
                    className={styles.input}
                    placeholder="Поиск"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                />
                <button className={styles.findButton} onClick={handleSearch}>
                    Найти
                </button>
                <select 
                    value={selectedFilter} 
                    onChange={e => handleFilter(e.target.value)}
                >
                    <option value="all">Без фильтров</option>
                    <option value='dog'>Только с собаками</option>
                    <option value='cat'>Только с котами</option>
                    <option value='lost'>Только потерянные</option>
                    <option value="found">Только найденные</option>
                </select>
            </div>
            
            {isLoading ? (
                <div>Загрузка...</div>
            ) : (
                <ul className={styles.list}>
                    {currReports.length > 0 ? (
                        currReports.map(report => 
                            <ReportItem key={report.id} report={report} />
                        )
                    ) : (
                        <div className={styles.noResults}>
                            Нет объявлений, соответствующих выбранным фильтрам
                            <button 
                                onClick={() => handleFilter('all')}
                                className={styles.resetButton}
                            >
                                Сбросить фильтры
                            </button>
                        </div>
                    )}
                </ul>
            )}
        </div>
    );
}
 
export default ReportList;